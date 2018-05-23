import sys
import time
import win32gui
import pyautogui
from time import sleep
import cv2
import mss
import numpy
import press_keys
import pytesseract
from PIL import Image


def take_base_screenshot(region):
    outFile = pyautogui.screenshot('ImageFile.png', region)


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_window_to_front(app_name):
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if i[1]:
            # print i[1]
            if app_name.lower() in i[1].lower():
                # print i
                win32gui.ShowWindow(i[0], 5)
                win32gui.SetForegroundWindow(i[0])
                break


def image_in_image_find(ref,new):
    method = cv2.CV_TM_SQDIFF_NORMED

    # Read the images from the file
    # small_image = cv2.imread('small_image.png')
    # large_image = cv2.imread('large_image.jpeg')
    small_image = cv2.imread(ref)
    large_image = cv2.imread(new)
    result = cv2.matchTemplate(small_image, large_image, method)
    return result


def image_loop(dict,event):
    threshold = 0.99
    method = cv2.TM_CCOEFF_NORMED
    template = cv2.imread('speed_25.png', 0)
    w, h = template.shape[::-1]
    end_max_val = 0
    with mss.mss() as sct:
        # Part of the screen to capture
        # monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 640}
        monitor = {'top': 450, 'left': 1730, 'width': 250, 'height': 250}
        exit_loop = 0
        while 'Screen capturing':
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))
            imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


            # result = cv2.matchTemplate(imgG,template,method)

            for key in dict.keys():
                tmp_img = cv2.imread(key,0)
                result = cv2.matchTemplate(imgG,tmp_img,method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val >= threshold:
                    event = False
                    dict[key] += 1
                    update_file("run_log.txt",key)
                    break

            # print min_val, max_val, min_loc, max_loc
            # showes red rectangle of the detected object
            # loc = numpy.where(result >= threshold)
            # for pt in zip(*loc[::-1]):
            #     cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            # Display the picture
            # cv2.imshow('OpenCV/Numpy normal', img)
            # if max_val >= threshold:
                # sys.exit()

            # Press "q" to quit
            if (cv2.waitKey(25) & 0xFF == ord('q')) or exit_loop >= 0:
                cv2.destroyAllWindows()
                end_max_val = max_val
                break
            exit_loop += 1
    return event,end_max_val,imgG


def press_ones_key(hex):
    press_keys.PressKey(hex)
    press_keys.ReleaseKey(hex)


def finish_quest_open_ship_info():
    press_ones_key(0x2E)  # c
    press_ones_key(0x2E)  # c
    press_ones_key(0x2E)  # c
    sleep(1)
    press_ones_key(0x05)  # 4
    press_ones_key(0x02)  # 1
    press_ones_key(0x02)  # 1
    sleep(1)
    press_ones_key(0x26)  # l
    press_ones_key(0x1C)  # enter
    press_ones_key(0x1C)  # enter
    press_ones_key(0xD1)  # PgDn


def load_game():
    press_keys.PressKey(0x2A)  # shift
    press_ones_key(0x26)  # l
    press_keys.ReleaseKey(0x2A)  # shift
    press_ones_key(0x1C)  # enter
    press_ones_key(0x1C)  # enter


def save_game():
    press_keys.PressKey(0x2A)  # shift
    press_ones_key(0x1F)  # s
    press_keys.ReleaseKey(0x2A)  # shift
    press_ones_key(0x1C)  # enter
    press_ones_key(0x1C)  # enter


def test():
    pyautogui.moveTo(2000, 400)
    pyautogui.click()
    sleep(1)
    finish_quest_open_ship_info()


def main():
    pyautogui.moveTo(2300, 400)
    pyautogui.click()
    sleep(1)
    loop_number = 1
    image_list = [
        "169.1.png",
        "175.8.png",
        "182.6.png",
        "189.4.png",
        "196.1.png",
        "202.9.png",
        "209.7.png",
        "216.4.png",
        "223.2.png",
        "230.0.png",
        "236.7.png",
        "243.5.png",
        "250.2.png"
        ]
    dict = {}
    for item in image_list:
        dict[item]=0

    while True:
        last_time = time.time()
        event = True
        load_game()
        sleep(25)
        finish_quest_open_ship_info()
        sleep(1)
        event,max_val, imgG = image_loop(dict,event)

        # if max_val not in dict.keys():
        #     dict[max_val] = 1
        #     cv2.imwrite("%s.png"%max_val,imgG)
        # else:
        #     dict[max_val] = dict[max_val]+1
        # print pytesseract.image_to_string(imgG)

        print ("\nloop:%s\nloop time:%s")%(loop_number, time.time() - last_time)
        for key in dict.keys():
            print ("%s :%s")%(key,dict[key])

        loop_number += 1

        # if dict["speed_25.png"] or dict["243.5.png"]:
        if event or dict["250.2.png"]:
            save_game()
            sys.exit()


def tessa():

    image = cv2.imread('speed_16.png')
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    print pytesseract.image_to_string(image)


def graph():
    y=[
        169.1,
        175.8,
        182.6,
        189.4,
        196.1,
        202.9,
        209.7,
        216.4,
        223.2,
        230.0,
        236.7,
        243.5
    ]
    x=[
        2218,
        428 ,
        359 ,
        263 ,
        186 ,
        123 ,
        75  ,
        57  ,
        32  ,
        13  ,
        6   ,
        2

    ]
    import numpy as np
    import random
    from matplotlib import pyplot as plt

    # data = np.random.normal(0, 20, 1000)

    # fixed bin size
    bins = np.arange(169, 250, 5)  # fixed bin size

    # plt.xlim([min(data) - 5, max(data) + 5])

    # plt.hist(data, bins=bins, alpha=0.5)
    # plt.plot(x,y)
    plt.title('hiperion results')
    plt.xlabel('variable X (bin size = 5)')
    plt.ylabel('count')
    # plt.bar(y, x, align='center')
    plt.bar(y, x)
    plt.show()


def update_file(log_file,data):
    import fileinput
    # log = open(log_file,"r").readlines()
    # print log
    for line in fileinput.FileInput(log_file,inplace=1):
        if data in line.split()[0]:
            x = int(line.split()[1]) + 1
            new_line = line.split()[0]+" "+str(x)+"\n"
            print new_line.strip()
            line.replace(line,new_line)
        else:
            print line.strip()


if __name__ == "__main__":
    app_name = "X3TC"
    main()
    # graph()
    # update_file("run_log.txt","169.1")

