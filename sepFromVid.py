import time

import cv2
import json
import rgb2blockid


def input_vid():
    starttime = time.time()
    print("start capture")
    cap = cv2.VideoCapture("lie.mp4")
    # cap = cv2.VideoCapture("newYear.mp4")
    ret = True
    imgs = []
    i = 0
    while ret:
        ret, img = cap.read()
        if ret:
            i+=1
            print(f"\rGet new pic {i}", end="")
            imgs.append(cv2.cvtColor(cv2.resize(img, (96, 54)), cv2.COLOR_RGB2BGR) / 255)
    print(f"\nEnd capture with time {time.time() - starttime}")
    starttime = time.time()
    m = rgb2blockid.matchBlock()
    pics = []
    for i in range(len(imgs)):
        starttime = time.time()
        pics.append(m.matchPicture(imgs[i]))
        print(f"\n{i + 1}/{len(imgs)}:{round((i + 1) / len(imgs) * 100, 2)}%\t-------------------------{time.time() - starttime}")
        if i % 10 == 0:
            with open("cache.json", "w") as f:
                f.write(json.dumps(pics))
    with open("happyNewYear.json", "w") as f:
        f.write(json.dumps(pics))


def output(prefix=True):
    if prefix:
        with open(f"/Users/lishuyu/Downloads/{input()}", "r") as f:
            pics = json.loads(f.read())
    else:
        with open("happyNewYear.json", "r") as f:
            pics = json.loads(f.read())
    for i in range(len(pics)):
        pic = pics[i]
        s = "# minecraft convert save.json to command lines\n"
        for row in range(len(pic)):
            for col in range(len(pic[0])):
                id = pic[row][col]['id']
                s += f"setblock {col} {0} {row} {id}\n"
                if id == "gravel" or id == "sand":
                    s += f"setblock {col} {-1} {row} stone\n"
        file_path = "/Users/lishuyu/Library/Application Support/minecraft/saves/虚空/datapacks/test/data/custom/functions/"
        with open(file_path + f"pic{i}.mcfunction", "w") as f:
            f.write(s)

    s = ""
    s_cla = ""
    file_path = "/Users/lishuyu/Library/Application Support/minecraft/saves/虚空/datapacks/test/data/custom/functions/"
    for i in range(len(pics)):
        s += f"schedule function custom:pic{i} {i + 5}s\n"
        s_cla += f"schedule clear custom:pic{i}\n"
    with open(file_path + f"pic.mcfunction", "w") as f:
        f.write(s)
    with open(file_path + f"cla.mcfunction", "w") as f:
        f.write(s_cla)


if __name__ == '__main__':
    start_time = time.time()
    # input_vid()
    output()
    print(time.time() - start_time)
