import re
import torch

class RegexTextExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "pattern": ("STRING", {"default": r'"第一帧描述": "(.*?)"'}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")

    FUNCTION = "extract"
    CATEGORY = "text/processing"

    def extract(self, text, pattern):
        try:
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                # 清理结果：去除可能的引号和前后空格
                cleaned = [match.strip('"\' \n') for match in matches]
                return (
                cleaned[0] if len(cleaned) > 0 else "",
                cleaned[1] if len(cleaned) > 1 else "",
                cleaned[2] if len(cleaned) > 2 else "",
                cleaned[3] if len(cleaned) > 3 else ""
            )
            return ("", "", "", "")
        except Exception as e:
            print(f"Regex extraction error: {str(e)}")
            return ("", "", "", "")

NODE_CLASS_MAPPINGS = {
    "RegexTextExtractor": RegexTextExtractor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RegexTextExtractor": "🔍 Regex Text Extractor"
}
    