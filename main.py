import glob
import json
import threading
import time
from os import path

import cv2
import matplotlib.colors as col
import matplotlib.pyplot as plt
import numpy as np

assert path.exists("minecraft/blockstates")
assert path.exists("minecraft/models/block")
assert path.exists("minecraft/textures/block")


def update():
    dictionary = []

    for name in glob.glob("minecraft/blockstates/*"):
        with open(name, "r") as f:
            data = json.loads(f.read())
        if "glass" in name or "spawner" in name or "egg" in name:
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
        with open(data.replace("minecraft:block", "minecraft/models/block") + ".json", "r") as f:
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
        # minecraft/textures/block/acacia_log_top.png

        if texture.startswith("minecraft:block"):
            texture = texture.replace("minecraft:block", "minecraft/textures/block")
        elif texture.startswith("block/"):
            texture = texture.replace("block/", "minecraft/textures/block/")
        assert texture.startswith("minecraft/textures/block/")
        texture = texture + ".png"
        print(texture, end="\t")
        img = plt.imread(texture)
        avg = np.average(img, axis=(0, 1))

        if data.startswith("minecraft:block/"):
            data = data.replace("minecraft:block/", "")
        elif data.startswith("block/"):
            data = data.replace("block/", "")

        if avg.shape == (4,):
            avg = col.to_rgb(avg)
            dictionary.append({"id": data, "texture": texture, "avg": list(avg)})
        else:
            dictionary.append({"id": data, "texture": texture, "avg": avg.tolist()})
        print(list(avg))

    with open("block_color.json", "w") as f:
        f.write(json.dumps(dictionary))


class matchBlock:
    def __init__(self):
        with open("block_color.json", "r") as f:
            self.dictionary = json.loads(f.read())
        self.Lock = threading.BoundedSemaphore(10)

    def find(self, rgb, save=False, row=None, col=None):
        rgb = np.array(rgb)
        match = self.dictionary[0]
        error = np.sum(np.abs(np.array(self.dictionary[0]["avg"]) - rgb))
        for color in self.dictionary:
            new_error = np.sum(np.abs(np.array(color["avg"]) - rgb))
            if new_error < error:
                match = color
                error = new_error
        if save:
            self.pic[row][col] = match
            self.Lock.release()
        else:
            self.Lock.release()
            return match

    def matchPicture(self, img):
        """
        Input an rbg picture, reture block id need be placed
        :param img: rbg
        :return: block id need be placed
        """

        def eachcolprogress(row_t):
            process_t = []

            for col in range(len(img[0])):
                self.Lock.acquire()
                t = threading.Thread(target=self.find, args=(img[row_t][col], True, row_t, col,))
                t.start()
                # print(f"\r{row_t},{col},{threading.active_count()}", end="\t")
                process_t.append(t)

            for t in process_t:
                t.join()

        self.pic = np.zeros((len(img), len(img[0]))).tolist()
        process = []
        for row in range(len(img)):
            t = threading.Thread(target=eachcolprogress, args=(row,))
            t.start()
            process.append(t)
        for t in process:
            t.join()
        return self.pic

class stream:
    def __init__(self):
        self.img = None
        threading.Thread(target=self.capStart).start()
        self.m = matchBlock()
    def capStart(self):
        cap = cv2.VideoCapture(1)
        while True:
            ret, img = cap.read()
            if ret:
                self.img = cv2.cvtColor(cv2.resize(img, (48,27)), cv2.COLOR_RGB2BGR)/255
            cv2.waitKey(1000)

    def output(self, pic):
        s = "# minecraft convert save.json to command lines\n"
        s_cla = "# minecraft reset program"
        for row in range(len(pic)):
            for col in range(len(pic[0])):
                id = pic[row][col]['id']
                s += f"setblock {row} {0} {-col} {id}\n"
                s_cla += f"setblock {row} {0} {-col} air\n"
                if id == "gravel" or id == "sand":
                    s += f"setblock {row} {-1} {-col} stone\n"
        file_path = "/Users/lishuyu/Library/Application Support/minecraft/saves/虚空/datapacks/test/data/custom/functions/"
        with open(file_path + "pic.mcfunction", "w") as f:
            f.write(s)
        with open(file_path + "cla.mcfunction", "w") as f:
            f.write(s_cla)
        print("Loop")

    def main(self):
        while True:
            if self.img is None:
                time.sleep(1)
                continue
            pic = self.m.matchPicture(self.img)
            threading.Thread(target=self.output, args=(pic,)).start()

if __name__ == '__main__':
    # update()
    s = stream()
    s.main()