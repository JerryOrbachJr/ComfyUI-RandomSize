import yaml, os, random
module_root_directory = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(module_root_directory,'sizes.yaml')

def read_config(item):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)[item]

class RandomSize:
    CATEGORY = "utils"
    def INPUT_TYPES(cls):
        return {
            "required": {},
        }
    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")
    FUNCTION = "func"
    def func(self,size:str):
        sizes = read_config('sizes')
        rand_obj = random.random.Random()
        idx = rand_obj.randint(0, len(sizes))
        size = sizes[idx]
        x, y = [int(v) for v in size.split('x')]
        return (x,y)
    
