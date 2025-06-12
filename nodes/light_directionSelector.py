import torch
import comfy
import comfy.utils

class DirectionSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_lu": ("IMAGE",),
                "image_u": ("IMAGE",),
                "image_ru": ("IMAGE",),
                "image_l": ("IMAGE",),
                "image_r": ("IMAGE",),
                "image_ld": ("IMAGE",),
                "image_d": ("IMAGE",),
                "image_rd": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("direction",)
    FUNCTION = "select_direction"
    
    CATEGORY = "NVVS/image processing"
    
    def select_direction(self, image_lu, image_u, image_ru, image_l, image_r, image_ld, image_d, image_rd):
        # 计算每张图像的黑色区域面积
        a = self.calculate_black_area(image_lu)
        b = self.calculate_black_area(image_u)
        c = self.calculate_black_area(image_ru)
        d = self.calculate_black_area(image_l)
        e = self.calculate_black_area(image_r)
        f = self.calculate_black_area(image_ld)
        g = self.calculate_black_area(image_d)
        h = self.calculate_black_area(image_rd)
        
        # 找出最小面积的方向
        direction = self.find_min_and_output_lu(a, b, c, d, e, f, g, h)
        return (direction,)
    
    def calculate_black_area(self, image_tensor):
        """计算图像中黑色区域的面积"""
        # 确保处理的是单张图像（去除批次维度）
        if image_tensor.dim() == 4:
            image_tensor = image_tensor.squeeze(0)
            
        # 转换为灰度图（如果输入是彩色图）
        if image_tensor.size(-1) == 3:
            # 使用标准RGB转灰度公式
            gray_image = 0.2989 * image_tensor[..., 0] + 0.5870 * image_tensor[..., 1] + 0.1140 * image_tensor[..., 2]
        elif image_tensor.size(-1) == 1:
            gray_image = image_tensor[..., 0]
        else:
            # 对于其他通道数，取平均值
            gray_image = torch.mean(image_tensor, dim=-1)
        
        # 设定黑色阈值（50/255）
        threshold = 50.0 / 255.0
        black_pixels = gray_image < threshold
        return torch.sum(black_pixels).item()
    
    def find_min_and_output_lu(self, a, b, c, d, e, f, g, h):
        """找出最小面积对应的方向标签"""
        values = [a, b, c, d, e, f, g, h]
        min_value = min(values)
        min_indices = [i for i, v in enumerate(values) if v == min_value]
        labels = ['LU', 'U', 'RU', 'L', 'R', 'LD', 'D', 'RD']
        return labels[min_indices[0]]
