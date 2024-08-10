import yaml, os, random
from server import PromptServer
from aiohttp import web
sizes_dir = os.path.join(os.path.dirname(__file__), "sizes")
sizes_dir = os.path.abspath(sizes_dir)
custom_sizes_dir = os.path.join(os.path.dirname(__file__), "sizes","custom")
custom_sizes_dir = os.path.abspath(custom_sizes_dir)


def get_sizes_from_preset_file(preset_file):
    if not preset_file or preset_file == "Preset":
        preset_file_path = os.path.join(sizes_dir, "SD1.5.yaml")
    else:
        preset_file_path = os.path.join(custom_sizes_dir, preset_file)

        if not os.path.exists(preset_file_path):
            preset_file_path = os.path.join(sizes_dir, preset_file)

            if not os.path.exists(preset_file_path):
                raise FileNotFoundError(f"Preset file '{preset_file}' not found in either {sizes_dir} or {custom_sizes_dir}.")

    with open(preset_file_path, 'r') as file:
        return yaml.safe_load(file)['sizes']


def load_presets():
    default_list = [dfile for dfile in os.listdir(sizes_dir) if dfile.endswith(".yaml")]
    user_list = [ufile for ufile in os.listdir(custom_sizes_dir) if ufile.endswith(".yaml")]
    return default_list + user_list


@PromptServer.instance.routes.post("/JOJR_RandomSize/get_sizes")
async def get_sizes_endpoint(request):
    data = await request.json()
    preset = data.get("preset")

    sizes = get_sizes_from_preset_file(preset)
    return web.json_response(sizes)


class RandomSize:
    CATEGORY = "utils"
    @classmethod
    def INPUT_TYPES(cls):
        preset = ["Preset"]
        preset += load_presets()
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "preset": (preset,)
            },
            "hidden": {"id":"UNIQUE_ID"}
        }
    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")
    FUNCTION = "func"
    def func(self:str,seed, preset,id):
        sizes = get_sizes_from_preset_file(preset)

        if 0 <= seed < len(sizes):
            size = sizes[seed]
        else:
          rand_obj = random.Random(seed)
          size = rand_obj.choice(sizes)

        for i in range(len(sizes)):
            if sizes[i] == size:
                sizes[i] = f"*{size}*"

        PromptServer.instance.send_sync("jojr.random-sizes.sendmessage", {"id": id, "message":sizes})
        w, h = [int(i) for i in size.split('x')]
        return (w,h)