import pyautogui
from time import sleep
import cv2
import numpy as np
import pyperclip
import keyboard

f = open('data.txt', 'r')
num = f.read()
num = num.split()
num = num[2]
num = int(num)
currFollowed = num  # LIMIT TO AROUND 350
allfollowed = open('allfollowed.txt', 'r+')


def follow():
    sleep(5)
    pyautogui.PAUSE = 1.0
    locate_user()

########## You can ignore most of this
def click_explore(images):
# Click on the explore button
    sleep(3)
    explorebtn = pyautogui.locateOnScreen(images.get("explorebtn"))
    while explorebtn is None:
        print("ERROR: Can not locate Twitter window.\n Bring on screen or scale to full screen.\n")
        sleep(4)
        explorebtn = pyautogui.locateOnScreen(images.get("explorebtn"))
    pyautogui.click(pyautogui.center(explorebtn))


def click_trends(images):
# Click on the first trending topic
    trends = pyautogui.locateOnScreen(images.get("trendsforyou"))
    while trends is None:
        print("ERROR: Can not locate Twitter window.\n Bring on screen or scale to full screen.\n")
        sleep(4)
        trends = pyautogui.locateOnScreen(images.get("trendsforyou"))
    pyautogui.click(trends[1], trends[2]-20)


def click_latest(images):
# Click on the latest tweets tab
    latest = pyautogui.locateOnScreen(images.get("latest"))
    while latest is None:
        print("ERROR: Can not locate Twitter window.\n Bring on screen or scale to full screen.\n")
        sleep(4)
        latest = pyautogui.locateOnScreen(images.get("latest"))
########################################


def savedata():
    f = open('data.txt', 'r+')
    num = f.read()
    num = num.split()
    num = num[2]
    n = num
    num = int(num) + 1
    s = "Users Followed: " + str(num)
    print(s)
    f.seek(0)
    f.write(s)
    f.truncate()
    f.close()


def FFCount(s):
    s = s.strip()
    s = s.replace(',', '')
    s = s.split()

    num1 = s[0]
    num2 = s[2]
    if 'M' in num1:
        return False
    if 'K' in num1:
        num1.replace('K', '')
        if '.' in num1:
            num1 = num1.replace('.', '')
            num1 += num1+'00'
        else:
            num1 += num1+'000'
    if 'K' in num2:
        num2.replace('K', '')
        if '.' in num2:
            num2 = num2.replace('.', '')
            num2 += num2+'00'
        else:
            num2 += num2+'000'
    if num1.isnumeric() and num2.isnumeric():
        num1 = float(num1)
        num2 = float(num2)
        num3 = num2 - num1
        num4 = num1 / num2

        if num3 < 100 or num4 > .85:
            return True
        else:
            return False
    else:
        return False


def locate_user():
    while keyboard.is_pressed('q') is not True and currFollowed <= 350:
        pyautogui.hotkey('f5')
        sleep(5)

        # Find all of the @ symbols on the page
        pyautogui.screenshot('img/screenshot.png')
        img_rgb = cv2.imread('img/screenshot.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('img/atsign.png', 0)
        #w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        #for pt in zip(*loc[::-1]):
        #    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        #cv2.imwrite('res.png', img_rgb)

        keepitgoing(zip(*loc[::-1]))


def keepitgoing(loc):
    for pt in loc:
        try:
            global currFollowed
            f = open('allfollowed.txt', 'a+')
            if keyboard.is_pressed('q') or currFollowed >= 350:
                print("Daily follow limit reached (350).\nEdit data.txt to follow more.")
                savedata()
                f.close()
                quit()

            # gets the link location so we can easily get the username
            pyautogui.moveTo(pt[0] + 10, pt[1] + 5)
            pyautogui.rightClick()
            pyautogui.screenshot('img/screenshot.png')
            img_rgb = cv2.imread('img/screenshot.png')
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread('img/copylinklocation.png', 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            if len(loc[0]) == 0:
                break

            for npt in zip(*loc[::-1]):
                pyautogui.moveTo(npt[0], npt[1] + 5)
                pyautogui.click()
                pyautogui.moveRel(-500)
                break
            pyautogui.moveTo(pt[0] + 10, pt[1] + 5)
            namelink = pyperclip.paste()
            namelink = namelink.split('/')
            namelink = namelink[len(namelink)-1]
            namelink = '@' + namelink

            global allfollowed
            if namelink in allfollowed:
                break

            # Finds the text "Not followed by anyone"
            # which is typically found on the bottom of every user when the mouse hovers over their name.
            sleep(2)
            pyautogui.screenshot('img/screenshot.png')
            img_rgb = cv2.imread('img/screenshot.png')
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread('img/notfollowedbyanyone.png', 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            if len(loc[0]) == 0:
                break

            for npt in zip(*loc[::-1]):
                pyautogui.moveTo(npt[0], npt[1] + 5)
                break

            pyautogui.moveRel(0, -25)
            pyautogui.dragRel(275, 0, duration=1)
            pyautogui.hotkey('ctrl', 'c')
            text = pyperclip.paste()

            try:
                # If follower / following ratio is good, it'll follow them
                if FFCount(text):
                    pyautogui.screenshot('img/screenshot.png')
                    img_rgb = cv2.imread('img/screenshot.png')
                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                    template = cv2.imread('img/followBtn.png', 0)
                    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.8
                    loc = np.where(res >= threshold)

                    if len(loc[0]) == 0:
                        break

                    for npt in zip(*loc[::-1]):
                        pyautogui.moveTo(npt[0] + 10, npt[1] + 10)
                        break
                    pyautogui.click()

                    currFollowed += 1
                    savedata()

                    f.write(namelink + '\n')
                    print("following {}".format(namelink))
            except IndexError:
                pyautogui.moveRel(-500)
                break

            pyautogui.moveRel(-750, 0)
        except():
            pass
