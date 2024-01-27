import yaml, os, random
module_root_directory = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(module_root_directory,'sizes.yaml')
# TODO: make inputs?
def read_config(item):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)[item]

class RandomSize:
    CATEGORY = "utils"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}) },
        }
    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")
    FUNCTION = "func"
    def func(self:str,seed):
        sizes = read_config('sizes')
        rand_obj = random.Random(seed)
        size = rand_obj.choice(sizes)
        x, y = [int(v) for v in size.split('x')]
        return (x,y)
    
