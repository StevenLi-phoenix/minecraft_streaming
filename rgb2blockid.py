import json
import time


class matchBlock:
    def __init__(self, img_x, img_y):
        self.img_x = img_x
        self.img_y = img_y
        print("Start loading Dictionary")
        with open("dictionary_rgb.json", "r") as f:
            self.rgb = json.loads(f.read())
            print("Loaded Dictionary")
        self.progress_list = []
        for row in range(img_x):
            for col in range(img_y):
                self.progress_list.append([row, col])

    def matchPicture(self, img):
        self.pic = [[0 for _f in range(self.img_y)] for _i in range(self.img_x)]
        for value in self.progress_list:
            self.find(img[value[0]][value[1]].tolist(), value)
        return self.pic

    def find(self, rgb, value):
        assert type(rgb[0]) == int and type(rgb[1]) == int and type(rgb[2]) == int
        self.pic[value[0]][value[1]] = self.rgb[f"{rgb[0]},{rgb[1]},{rgb[2]}"]


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    img = plt.imread("pack.png")
    if not img.shape[2] == 3:
        img = img[:,:,:3]
    starttime = time.time()
    m = matchBlock(img.shape[0], img.shape[1])
    print(f"Load time: {round(time.time() - starttime, 2)}s")
    starttime = time.time()
    pic = m.matchPicture(img)
    print(f"Progress time: {round(time.time() - starttime, 2)}s")
    print(str(pic))
