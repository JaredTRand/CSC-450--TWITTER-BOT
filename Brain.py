from Bot import TwitterBot
import cv2
import pyautogui
import numpy as np
from time import sleep


def swap_user(user):
    loc = locate_image('morebtn', .8)
    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0] + 10, npt[1] + 20)
        pyautogui.click()
        sleep(.2)
        pyautogui.click()
        break
    sleep(.3)
    loc = locate_image('logoutbtn', .8)
    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0] + 30, npt[1] + 20)
        pyautogui.click()
        break
    sleep(2)
    loc = locate_image('usernameentry', .8)
    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0] + 30, npt[1] + 20)
        pyautogui.click()
        pyautogui.typewrite(user.credentials[0])

        sleep(1)
        pyautogui.moveRel(250)
        pyautogui.click()
        pyautogui.typewrite(user.credentials[1])
        pyautogui.hotkey('enter')
        sleep(1)
        break


def locate_image(imgname, threshold):
    pyautogui.screenshot('img/screenshot.png')
    img_rgb = cv2.imread('img/screenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('img/{}.png'.format(imgname), 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return loc


# Write stuff for the bot to do here
# (follow, unfollow, swapuser)
if __name__ == '__main__':
    bot1 = TwitterBot(user=0)
    bot1.follow()


