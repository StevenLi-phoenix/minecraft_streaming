import json
import numpy as np
import threading

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


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    img = plt.imread("sample.jpg")/255
    m = matchBlock()
    pic = m.matchPicture(img)
    with open("save.json", "w") as f:
        f.write(json.dumps(pic))
