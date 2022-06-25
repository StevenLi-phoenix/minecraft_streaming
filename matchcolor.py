from tqdm import tqdm
from json import load, dump

block_colors = load(open("block_color.json", "r"))
rgb_list = [(r, g, b) for r in range(256) for g in range(256) for b in range(256)]

def calculate_distance(point1, point2) -> float:
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    x1, y1, z1 = x1*255, y1*255, z1*255
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5
    return distance

rgb_dictionary = {}
for r_bins in range(256):
    rgb_dictionary[r_bins] = {}
    for g_bins in range(256):
        rgb_dictionary[r_bins][g_bins] = {}
        for b_bins in range(256):
            rgb_dictionary[r_bins][g_bins][b_bins] = ""


for rgb in tqdm(rgb_list, mininterval=1):
    min_dis = 444 # diagonal length
    selection = block_colors[0] #'gray_concrete'
    for block_color in block_colors:
        cur_dis = calculate_distance(block_color["avg"], rgb)
        if cur_dis < min_dis:
            min_dis = cur_dis
            selection = block_color
    rgb_dictionary[rgb[0]][rgb[1]][rgb[2]] = selection["id"]

dump(rgb_dictionary, open("dictionary_rgb.json","w"))