
from .random_size import RandomSize
LIVE_NODE_CLASS_MAPPINGS = {
    "JOJR_RandomSize": RandomSize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JOJR_RandomSize": "Random Size",
}
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']