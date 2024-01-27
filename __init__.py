
"""
@author: JerryOrbachJr
@title: Random Size
@nickname: Random Size
@description: A ComfyUI custom node that randomly selects a height and width pair from a list in a config file
"""

from .random_size import RandomSize
NODE_CLASS_MAPPINGS = {
    "JOJR_RandomSize": RandomSize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JOJR_RandomSize": "Random Size",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']