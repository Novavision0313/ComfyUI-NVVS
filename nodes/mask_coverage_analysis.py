import torch
from server import PromptServer
from aiohttp import web
import torch

class MaskCoverageAnalysis:
    @classmethod
    def INPUT_TYPES(cls):
        # threshold 判断黑白的阈值   默认为0  表示大于0的即为白区
        return {
            "required": {
                "mask": ("MASK",),
                "threshold": ("FLOAT", {
                    "default": 0, 
                    "min": 0.00, 
                    "max": 1.00,
                    "step": 0.01,
                    "display": "slider"
                }),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("coverage",)
    FUNCTION = "mask_coverage_analysis"
    CATEGORY = "NVVS/mask processing"

    def mask_coverage_analysis(self, mask, threshold):
        # 维度标准化处理 (支持批量/单张输入)
        if mask.dim() == 4:    # [B, C, H, W]
            mask = mask.squeeze(1)  # 移除单通道
        elif mask.dim() == 2:  # [H, W]
            mask = mask.unsqueeze(0)  # 添加批次维度

        # 数值范围校验
        if mask.min() < 0 or mask.max() > 1:
            mask = torch.clamp(mask, 0, 1)
            print(f"⚠️ Mask values auto-clamped to [0,1] range")

        # 计算覆盖率（白区占比）
        white_pixels = torch.sum(mask > threshold).float()
        coverage = white_pixels / mask.numel()

        # 输出标准化数值（保留4位小数）
        return (round(coverage.item(), 4), )

