import time

import cv2
import json

from tqdm import tqdm

import rgb2blockid


def input_vid(seq=False, shape = (96, 54)):
    starttime = time.time()
    print("start capture")
    cap = cv2.VideoCapture("lie.mp4")
    ret = True
    imgs = []
    i = 0
    while ret:
        ret, img = cap.read()
        if ret:
            i += 1
            print(f"\rGet new frame {i}", end="")
            imgs.append(cv2.cvtColor(cv2.resize(img, shape), cv2.COLOR_RGB2BGR))
            if i == 3000: break
    print(f"\nEnd capture with time {time.time() - starttime}")
    m = rgb2blockid.matchBlock(shape[1], shape[0])
    print("Start progressing")
    pics = []
    for i in tqdm(range(len(imgs))):
        result = m.matchPicture(imgs[i])
        pics.append(result)
    if seq:
        output(pics=pics)
    else:
        with open("happyNewYear.json", "w") as f:
            f.write(json.dumps(pics))


def output(pics=None):
    print("Start output commands")
    if pics is None:
        print("start load dataset")
        with open("happyNewYear.json", "r") as f:
            pics = json.loads(f.read())
        print("loaded dataset done")
    print("start writing commands")
    assert pics[0] != pics[10]
    current_status = pics[0]
    for i in tqdm(range(len(pics))):
        pic = pics[i]
        s = f"# minecraft convert save.json to command lines command {i}\n"
        for row in range(len(pic)):
            for col in range(len(pic[0])):
                id = pic[row][col]
                if id != current_status[row][col] or i == 0:
                    current_status[row][col] = id
                    s += f"setblock {col} {0} {row} {id}\n"
        file_path = "/Users/lishuyu/Library/Application Support/minecraft/saves/虚空/datapacks/test/data/custom/functions/"
        with open(file_path + f"pic{i}.mcfunction", "w") as f:
            f.write(s)

    print("start establish schedule and clear commands")
    s = "fill 95 -1 53 0 -1 0 stone\ngamemode spectator @a\ntp @a 48.0 27.5 27.0 -180 90\n"
    s_cla = "gamemode creative @a\n"
    file_path = "/Users/lishuyu/Library/Application Support/minecraft/saves/虚空/datapacks/test/data/custom/functions/"
    for i in tqdm(range(len(pics))):
        s += f"schedule function custom:pic{i} {i + 20}t\n"
        s_cla += f"schedule clear custom:pic{i}\n"
    with open(file_path + f"pic.mcfunction", "w") as f:
        f.write(s)
    with open(file_path + f"cla.mcfunction", "w") as f:
        f.write(s_cla)


if __name__ == '__main__':
    start_time = time.time()
    input_vid(seq=True)
    # output()
    print("time record:", time.time() - start_time)
