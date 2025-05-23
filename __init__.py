from .nodes.all_black_mask_validator import *
from .nodes.string_preprocessing import *
from .nodes.mask_coverage_analysis import *
from .nodes.highlight_index_selector import *

NODE_CONFIG = {
    "AllBlackMaskValidator": {"class": AllBlackMaskValidator, "name": "All Black Mask Validator"},
    "StringSplit": {"class": StringSplit, "name": "String Split"},
    "StringStrip": {"class": StringStrip, "name": "String Strip"},
    "MaskCoverageAnalysis": {"class": MaskCoverageAnalysis, "name": "Mask Coverage Analysis"},
    "HighlightIndexSelector": {"class": HighlightIndexSelector, "name": "Highlight Index Selector"},
}
# "": {"class": , "name": ""},

def generate_node_mappings(node_config):
    node_class_mappings = {}
    node_display_name_mappings = {}

    for node_name, node_info in node_config.items():
        node_class_mappings[node_name] = node_info["class"]
        node_display_name_mappings[node_name] = node_info.get("name", node_info["class"].__name__)

    return node_class_mappings, node_display_name_mappings

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = generate_node_mappings(NODE_CONFIG)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]


# Example of adding a custom API route
@PromptServer.instance.routes.get("/custom_endpoint")
async def custom_endpoint(request):
    return web.json_response({"message": "This is a custom endpoint"})