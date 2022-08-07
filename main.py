from pyautogui import *
import time
import os
import sys
import cv2
import json

runtime = input("次數: ")
conf = float(input("信度: "))
sec = float(input("間隔秒數: "))
isGray = input("啟用灰度匹配 (Y/N): ").upper()
isGrayscale = False

def locate_click(imgname, alt=None, t=0.1, button="left"):

    time.sleep(t)

    img = cv2.imread(imgname)
    isGrayscale = True if isGray == 'Y' else 'N'
    # screenwidth,screenheight = size()
    # screenImg = screenshot()
    # screen_dpi = int(screenImg.size[0]/screenwidth)
    # print(screenwidth)
    # print(screenheight)
    # print(screen_dpi)
    # print(isGrayscale)

    box = locateOnScreen(img,confidence=conf, grayscale=isGrayscale)
    print(imgname, "found at:\n\t", box)

    if box is None:
        if alt is not None:
            locate_click(alt, button=button)
        
        print("找不到圖片" + imgname)
        return False

    x, y = box.left + box.width/2, box.top + box.height/2
    moveTo(x, y)
    long_click(button=button)
    return True

def long_click(t=0.100, button="left"):
    mouseDown(button=button)
    time.sleep(t)
    mouseUp(button=button)

# get root 
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

print("4秒後執行，請切換至FF14視窗")
time.sleep(4)


img_dir = application_path + "\\img\\"

f = open(application_path + '\\config.json')

jsonObject = json.load(f)

f.close()

for index in range(0, int(runtime)):

    start_x, start_y = size()
    start_x /= 3;
    start_y /= 2;
    moveTo(start_x, start_y)

    for i in jsonObject:
        type = i["type"]
        commmand = i["command"]
        dir = i["dir"]

        if type == "button":
            press(commmand)
        elif type == "image":
            path = img_dir + commmand
            if not locate_click(path, path, t=0.35, button = dir): 
                break;
        elif type == "long":
            long_click(button=dir)
        else:
            print("not defind")

        time.sleep(sec)

    print("done: " + str(index))
    time.sleep(3)

# import sys
# from control.ctr_main import Ctr_Main

# if __name__ == '__main__':
#     ctrMain = Ctr_Main()
#     sys.exit(main())


