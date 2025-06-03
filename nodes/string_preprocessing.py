import torch
from server import PromptServer
from aiohttp import web

class StringStrip():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": '', "multiline": True}),
                "chars": ("STRING", {"default": '', "multiline": False}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string_striped",)
    FUNCTION = "string_strip"
    CATEGORY = "NVVS/string processing"

    def string_strip(self, string, chars):
        print("-"*10)
        print(type(string), '+', type(chars))
        print("-"*10)
        print("string.strip(): ", string.strip())
        print("-"*10)
        print("string.strip(chars): ", string.strip(chars))
        print("-"*10)
        if chars == '':
            result = string.lstrip().rstrip()
        else:
            result = string.slstrip(chars).rstrip(chars)
        return (result)
    

class StringSplit():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": '', "multiline": True}),
                "sep": ("STRING", {"default": '', "multiline": False}),
            }
        }
    RETURN_TYPES = ("tuple",)
    RETURN_NAMES = ("strings_turple",)
    FUNCTION = "string_split"
    CATEGORY = "NVVS/string processing"

    def string_split(self, string, sep):
        # 处理空分隔符的情况
        if sep == "":
            parts = string.split()
        else:
            parts = string.split(sep)

        # 返回一个包含字符串元组的元组，确保类型匹配
        return (tuple(parts), )

