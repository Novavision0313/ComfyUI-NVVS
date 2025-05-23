import torch

class HighlightIndexSelector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "highlight_ratios": ("FLOAT", {"forceInput": True, "vector": True}),
                "threshold": ("FLOAT", {
                    "default": 0.025,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.001,
                    "display": "slider"
                }),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("selected_index",)
    FUNCTION = "select_index"
    CATEGORY = "NVVS/mask processing"

    def select_index(self, highlight_ratios, threshold):

        print("-"*20)
        print("highlight_ratios: ", highlight_ratios, type(highlight_ratios))
        print("-"*20)

        # 类型转换和维度处理
        if isinstance(highlight_ratios, float):
            highlight_ratios = [highlight_ratios]  # 单个值转为列表
        elif isinstance(highlight_ratios, torch.Tensor):
            if highlight_ratios.dim() == 0:
                highlight_ratios = [highlight_ratios.item()]
            else:
                highlight_ratios = highlight_ratios.flatten().tolist()

        print("\n highlight_ratios: ", highlight_ratios, type(highlight_ratios))

        if not highlight_ratios:
            raise ValueError("ERROR: The input sequence cannot be empty!")

        for i in range(len(highlight_ratios)):
            selected_index = i-1 if i > 0 else 0
            
            if highlight_ratios[i] >= threshold:
                # 对比当前与前一帧的接近程度
                if i == 0:
                    break
                else:
                    selected_index = i if abs(highlight_ratios[i]-threshold) < abs(threshold-highlight_ratios[i-1]) else i-1
                    break
            if i == len(highlight_ratios):
                selected_index = i

        return (int(selected_index),)
        # return selected_index

# 本节点使用示例：
# [高光率序列] ➔ HighlightIndexSelector ➔ [选中的帧索引]
