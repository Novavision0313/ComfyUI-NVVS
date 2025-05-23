import torch
from server import PromptServer
from aiohttp import web

class AllBlackMaskValidator:
    """判断mask是否为全黑"""
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("shape_info", "is_all_black")
    FUNCTION = "all_black_mask_validator"
    CATEGORY = "NVVS/mask processing"

    def all_black_mask_validator(self, mask):
        # 获取输入mask的形状
        shape_info = f"Shape: {tuple(mask.shape)}"
        # 检查是否全黑（假设mask是单通道的）
        is_all_black = torch.all(mask == 0).item()
        # 如果mask是多通道的（非常用情况），改用：
        # is_all_black = torch.all(mask == 0, dim=[-1,-2]).all().item()
        return (shape_info, is_all_black)
    

