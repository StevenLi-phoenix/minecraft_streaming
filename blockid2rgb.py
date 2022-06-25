import glob
import json
from os import path

import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np

base = "assets"
path_blockstat = path.join(base, "minecraft/blockstates")
path_model_block = path.join(base, "minecraft/models/block")
path_textures_block = path.join(base, "minecraft/textures/block")
assert path.exists(path_blockstat)
assert path.exists(path_model_block)
assert path.exists(path_textures_block)

def update():
    dictionary = []

    for name in glob.glob(f"{path_blockstat}/*"):
        with open(name, "r") as f:
            data = json.loads(f.read())
        if "glass" in name:
            continue
        if "variants" in data.keys():
            data = data["variants"]
            if "" in data.keys():
                data = data[""]
                if type(data) == dict:
                    data = data["model"]
                else:
                    continue
            else:
                continue
        else:
            continue
        with open(data.replace("minecraft:block", f"{path_model_block}") + ".json", "r") as f:
            texture = json.loads(f.read())
        if "textures" in texture.keys():
            texture = texture["textures"]
            if "all" in texture.keys():
                texture = texture["all"]
            elif "end" in texture.keys():
                texture = texture["end"]
            else:
                continue
        else:
            continue
        # minecraft:block/acacia_log_top
        # path_textures_block/acacia_log_top.png

        if texture.startswith("minecraft:block"):
            texture = texture.replace("minecraft:block", path_textures_block)
        elif texture.startswith("block/"):
            texture = texture.replace("block", path_textures_block)
        assert texture.startswith(path_textures_block)
        texture = texture + ".png"
        print(texture, end="\t")
        img = plt.imread(texture)
        avg = np.average(img, axis=(0, 1))

        if data.startswith("minecraft:block/"):
            data = data.replace("minecraft:block/","")
        elif data.startswith("block/"):
            data = data.replace("block/","")

        if avg.shape == (4,):
            avg = col.to_rgb(avg)
            dictionary.append({"id": data, "texture": texture, "avg": list(avg)})
        else:
            dictionary.append({"id": data, "texture": texture, "avg": avg.tolist()})
        print(list(avg))

    with open("block_color.json", "w") as f:
        f.write(json.dumps(dictionary))

if __name__ == '__main__':
    update()