import json
import numpy as np
import threading
from tqdm import tqdm

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
                print(f"\r{row_t},{col},{threading.active_count()}", end="\t")
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

class matchBlockV2:
    def __init__(self, img_x, img_y):
        self.pic = np.zeros((img_x, img_y)).tolist()
        # with open("block_color.json", "r") as f:
        #     self.dictionary = json.loads(f.read())
        with open("dictionary_rgb.json", "r") as f:
            self.rgb = json.loads(f.read())
            print("Load Dictionary")

        """rgb_array = []
        for item in self.dictionary:
            rgb_array.append(item["avg"])
        rgb_array = np.array(rgb_array)
        self.DIClength = len(self.dictionary)

        def find(rgb):
            return self.dictionary[
                np.argmin(np.sum(np.abs(rgb_array - np.array([rgb for i in range(self.DIClength)])), axis=1))]["id"]

        self.dictionary_rgb = {}
        progress_list = []
        for r in range(256):
            for g in range(256):
                for b in range(256):
                    progress_list.append([r, g, b])
        for value in tqdm(progress_list):
            self.dictionary_rgb[f"{value[0]}, {value[1]}, {value[2]}"] = find(value)

        with open("dictionary_rgb.json", "w") as f:
            f.write(json.dumps(self.dictionary_rgb))"""

    def matchPicture(self, img):
        progress_list = []
        for row in range(len(img)):
            for col in range(len(img[0])):
                progress_list.append([row, col])
        for value in tqdm(progress_list):
            self.pic[value[0]][value[1]] = self.find(img[value[0]][value[1]].tolist())
        return self.pic

    def find(self, rgb, save=False, row=None, col=None):
        if save:
            self.pic[row][col] = self.rgb[f"{rgb[0]}, {rgb[1]}, {rgb[2]}"]
        else:
            return self.rgb[f"{rgb[0]}, {rgb[1]}, {rgb[2]}"]


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    img = plt.imread("sample.jpg")/255
    m = matchBlock()
    pic = m.matchPicture(img)
    with open("save.json", "w") as f:
        f.write(json.dumps(pic))
