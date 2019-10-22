import pyautogui
import  cv2
import numpy as np
from time import sleep
import pyperclip


def unfollow():
    pyautogui.PAUSE = .3

    pyautogui.screenshot('img/screenshot.png')
    img_rgb = cv2.imread('img/screenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('img/profile.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    #if len(loc[0]) == 0:

    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0], npt[1] + 5)
        pyautogui.moveRel(+10, +15)
        pyautogui.click()
        break

    sleep(3)

    pyautogui.screenshot('img/screenshot.png')
    img_rgb = cv2.imread('img/screenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('img/profilefollowers.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)

    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0], npt[1] + 5)
        pyautogui.moveRel(+5, +5)
        pyautogui.click()
        break

    sleep(3)

    pyautogui.screenshot('img/screenshot.png')
    img_rgb = cv2.imread('img/screenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('img/tweetbutton.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0], npt[1] + 5)
        pyautogui.moveRel(+50, +150)
        pyautogui.click()
        break

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    eew = str(pyperclip.paste())
    eew = eew.split()
    users = []
    for c in eew:
        if c.startswith('@'):
            users.append(c)

    f = open('followers.txt', 'r+')
    for i in users:
        f.write(i + '\n')
    f.close()

    pyautogui.click()

    pyautogui.screenshot('img/screenshot.png')
    img_rgb = cv2.imread('img/screenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('img/profilefollowing.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)

    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0], npt[1] + 5)
        pyautogui.moveRel(+5, +5)
        pyautogui.click()
        break
    sleep(2)

    pyautogui.PAUSE = .9
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.PAUSE = .3

    f = open('unfollowedcount.txt', 'r+')
    num = f.read()
    num = int(num)
    curunfollowed = num

    while curunfollowed <= 90:
        pyautogui.screenshot('img/screenshot.png')
        img_rgb = cv2.imread('img/screenshot.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('img/atSign.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = .9
        loc = np.where(res >= threshold)

        dothething(loc)
        pyautogui.scroll(1000)


def dothething(loc):
    f = open('followers.txt', 'r')
    g = f.read()
    f.close()

    f = open('unfollowedcount.txt', 'r+')
    num = f.read()
    num = int(num)
    curunfollowed = num

    for npt in zip(*loc[::-1]):
        if curunfollowed >= 90:
            print('Too many unfollowed today. Edit unfollowedcount.txt to unfollow more.')
            quit()
        pyautogui.moveTo(npt[0] - 4, npt[1] + 11)
        pyautogui.dragRel(300, 0, duration=.7)
        pyautogui.hotkey('ctrl', 'c')
        copy = pyperclip.paste()

        copy = copy.split()
        name = copy[len(copy)-1]
        n = open('unfollowedusers.txt')
        if name in g or 'Follows' in name or name in n.read():
            pass
        else:
            print('Unfollowing {}'.format(copy[len(copy)-1]))
            pyautogui.moveRel(165, -10)
            pyautogui.click()

            pyautogui.screenshot('img/screenshot.png')
            img_rgb = cv2.imread('img/screenshot.png')
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread('img/unfollowbtn.png', 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            for npt in zip(*loc[::-1]):
                pyautogui.moveTo(npt[0], npt[1] + 5)
                pyautogui.moveRel(+20, +20)
                pyautogui.click()
                break

            curunfollowed += 1
            f.seek(0)
            f.write(str(curunfollowed))
            f.truncate()

            s = open('unfollowedusers.txt', 'a+')
            s.seek(0)
            s.write(str(copy[len(copy)-1]) + '\n')
            s.truncate()
            s.close()

    f.close()

