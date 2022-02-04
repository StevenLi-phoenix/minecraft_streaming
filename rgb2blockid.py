import json
import time

import numpy as np
import threading
from tqdm import tqdm


class matchBlock:
    def __init__(self, img_x, img_y):
        self.pic = np.zeros((img_x, img_y)).tolist()
        print("Start Load Dictionary")
        with open("dictionary_rgb.json", "r") as f:
            self.rgb = json.loads(f.read())
            print("Loaded Dictionary")

    def matchPicture(self, img):
        progress_list = []
        for row in range(len(img)):
            for col in range(len(img[0])):
                progress_list.append([row, col])
        for value in progress_list:
            self.pic[value[0]][value[1]] = self.find(img[value[0]][value[1]].tolist())
        return self.pic

    def find(self, rgb):
        assert type(rgb[0]) == int and type(rgb[1]) == int and type(rgb[2]) == int
        return self.rgb[f"{rgb[0]},{rgb[1]},{rgb[2]}"]


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    img = plt.imread("sample.jpg")
    assert img.shape[2] == 3
    starttime = time.time()
    m = matchBlock(img.shape[0], img.shape[1])
    print(f"Load time: {round(time.time() - starttime, 2)}s")
    starttime = time.time()
    pic = m.matchPicture(img)
    print(f"Progress time: {round(time.time() - starttime, 2)}s")
    print(str(pic))
