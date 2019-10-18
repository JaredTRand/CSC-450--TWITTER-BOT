import pyautogui
import cv2
from time import sleep
import keyboard
import numpy as np


def clippaperclip():
    sleep(5)
    pyautogui.screenshot('img/screenshot.png')
    img_rgb = cv2.imread('img/screenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('img/paperclip.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    spacepress = False
    for pt in zip(*loc[::-1]):
        count = 0
        print("Clicking...")
        if spacepress:
            quit()
        while True:  # making a loop
            try:  # used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('q'):  # if key 'q' is pressed
                    spacepress = True
                    break  # finishing the loop
                else:
                    pyautogui.click(pt[0] + 20, pt[1] + 5)
            except:
                pass


if __name__ == '__main__':
    clippaperclip()
