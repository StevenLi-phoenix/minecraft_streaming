import glob
import os.path
import json
import time

import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import matplotlib.animation as animation

assert os.path.exists("assets/minecraft/blockstates")
assert os.path.exists("assets/minecraft/models/block")
assert os.path.exists("assets/minecraft/textures/block")

blockstates = os.listdir("assets/minecraft/blockstates")
model_block = os.listdir("assets/minecraft/models/block")
textures    = os.listdir("assets/minecraft/textures/block")

PATH_MINECRAFT = "assets/minecraft"
PATH_BLOCKSTATES = os.path.join(PATH_MINECRAFT, "blockstates")
PATH_MODELS = os.path.join(PATH_MINECRAFT, "models", "block")
PATH_TEXTURES = os.path.join(PATH_MINECRAFT, "textures", "block")

"""
{
  "variants": {
    "": {
      "model": "minecraft:block/brown_concrete"
    }
  }
}
"""
except_names = ["button","door","fence","seagrass","candle","pressure_plate","coral","slab","stairs","tulip","light",
                "air","water","item","bar","cocoa","anvil","flower","repeater","torch","tripwire","rail","wheat","piston",
                "pumpkin_stem","large_fern","sea_pickle","end_portal_frame","command_block","turtle_egg","rose",
                "pointed_dripstone","powder_snow_cauldron","cake","beehive","nether_wart","cave_vines","lilac","grass",
                "comparator","sweet_berry_bush","bell","snow","potatoes","carrots","beetroots","melon_stem","grindstone",
                "mycelium","jigsaw","lever","scaffolding","structure_block","small_dripleaf","soul_lantern","sculk_sensor",
                "big_dripleaf","mangrove_propagule","sculk_catalyst","peony","sculk_shrieker","farmland","leaves","spawner",
                # model too complex to include
                "redstone_lamp","podzol","observer","frosted_ice","lantern","respawn_anchor","bee_nest",]
all_valid_textures = []
fig, ax = plt.subplots(nrows = 15, ncols = 14)
figs_array = np.zeros((210,16,16,3)) # ignore Alpha value
for filename in os.listdir(PATH_BLOCKSTATES):
    next = False
    for name in except_names:
        if name in filename:
            next = True
            continue
    if next:
        continue
    blockstat = json.load(open(os.path.join(PATH_BLOCKSTATES, filename)))
    if "variants" not in blockstat.keys():
        continue
    blockstat_variants = blockstat["variants"]
    blockstat_variants_keys = blockstat_variants.keys()
    # print(blockstat_variants)
    model_name = ""
    if "" in blockstat_variants_keys:
        model_name = blockstat_variants[""]
    elif "facing=up" in blockstat_variants_keys:
        model_name = blockstat_variants["facing=up"]
    elif "facing=north" in blockstat_variants_keys:
        model_name = blockstat_variants["facing=north"]
    elif "axis=x" in blockstat_variants_keys:
        model_name = blockstat_variants["axis=x"]
    elif 'facing=east,lit=false' in blockstat_variants_keys:
        model_name = blockstat_variants['facing=east,lit=false']
    else:
        print(filename)
    if type(model_name) == list:
        model_name = model_name[0]
    model_name = model_name.get("model").split("/")[1]
    textures = json.load(open(os.path.join(PATH_MODELS, model_name)+".json"))["textures"]
    # only progress all
    textures_picture_path = textures.get("all")
    if textures_picture_path is not None:
        pass
        """textures_picture_path = textures_picture_path.split("/")[1]
        img = plt.imread(os.path.join(PATH_TEXTURES, textures_picture_path)+".png",format="png")
        print(filename, textures_picture_path)
        figs_array[len(all_valid_textures)] = img[:16,:16,:3]
        all_valid_textures.append(filename)"""
    else:
        print(textures)

"""figs_array = figs_array.reshape((15,14,16,16,3))
for row in range(15):
    for col in range(14):
        ax[row, col].imshow(figs_array[row, col, :, :, :].reshape(16,16,3))
        ax[row, col].axes.get_xaxis().set_visible(False)
        ax[row, col].axes.get_yaxis().set_visible(False)
print(len(all_valid_textures))
plt.show()
plt.imshow(np.average(figs_array, axis=(2,3)))
plt.show()
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
figs_array = np.average(figs_array, axis=(2,3)).reshape(210,3)
for i in range(210):
    d3fig = figs_array[i]
    ax.scatter(d3fig[0], d3fig[1], d3fig[2], color=d3fig)
ax.set_xlabel('R Label')
ax.set_ylabel('G Label')
ax.set_zlabel('B Label')"""
"""angle = 0
def rotate(num):
    ax.view_init(30, num)
    return [ax]
line_ani = animation.FuncAnimation(fig, rotate, frames=360,cache_frame_data=True,
                                   interval=5, blit=True)"""
# plt.show()

"""filenames = glob.glob(os.path.join(PATH_BLOCKSTATES,"*.json"))
material = ["_concrete.json","wool","stripped"]
material_block_ids = []
for filename in filenames:
    construct = False
    for m in material:
        if m in filename:
            construct = True
            continue
    if construct:
        material_block_ids.append(filename)
print(material_block_ids)"""



