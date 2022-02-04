import json
import time

import numpy as np
import threading
from tqdm import tqdm


class matchBlock:
    def __init__(self, img_x, img_y):
        # self.img_x = img_x
        # self.img_y = img_y
        self.pic = np.zeros((img_x, img_y)).tolist()
        with open("dictionary_rgb.json", "r") as f:
            self.rgb = json.loads(f.read())
            print("Loaded Dictionary")
        self.progress_list = []
        for row in range(img_x):
            for col in range(img_y):
                self.progress_list.append([row, col])

    def matchPicture(self, img):
        # self.pic = np.zeros((self.img_x, self.img_y)).tolist()
        for value in self.progress_list:
            self.find(img[value[0]][value[1]].tolist(), value)
        return self.pic

    def find(self, rgb, value):
        assert type(rgb[0]) == int and type(rgb[1]) == int and type(rgb[2]) == int
        self.pic[value[0]][value[1]] = self.rgb[f"{rgb[0]},{rgb[1]},{rgb[2]}"]


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
