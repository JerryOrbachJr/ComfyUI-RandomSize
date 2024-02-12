import yaml, os, random
sizes_dir = os.path.join(os.path.dirname(__file__), "sizes")
sizes_dir = os.path.abspath(sizes_dir)

def read_config(preset_file):
    if preset_file == "Preset":
        preset_file_path = os.path.join(sizes_dir,"SD1.5.yaml")
    else:
        preset_file_path = os.path.join(sizes_dir,preset_file)
    with open( preset_file_path, 'r') as file:
        return yaml.safe_load(file)['sizes']

def load_presets():
    preset_list = [file for file in os.listdir(sizes_dir) if file.endswith(".yaml")]
    return preset_list

class RandomSize:
    CATEGORY = "utils"
    @classmethod
    def INPUT_TYPES(cls):
        preset = ["Preset"]  # 20
        preset += load_presets()
        return {
            "required": { 
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "preset": (preset,)
            },
        }
    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")
    FUNCTION = "func"
    def func(self:str,seed, preset):
        sizes = read_config(preset)
        rand_obj = random.Random(seed)
        size = rand_obj.choice(sizes)
        x, y = [int(v) for v in size.split('x')]
        return (x,y)
    
