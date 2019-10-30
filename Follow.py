import pyautogui
from time import sleep
import cv2
import numpy as np
import pyperclip
import keyboard
from time import time
from datetime import datetime

f = open('data.txt', 'r')
num = f.read()
num = num.split()
num = num[2]
num = int(num)
currFollowed = num  # LIMIT TO AROUND 350
limit = 350
unfollowlimit = 85
allfollowed = open('allfollowed.txt', 'r+')

lasttimefollowed = open('latesttime.txt', )


def follow():
    sleep(1)
    pyautogui.PAUSE = .3
    loc = locate_image('tweetbutton', .8)
    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0], npt[1]+100)
        pyautogui.click()
        pyautogui.hotkey('f5')
        break

    locate_user()


def check_time(whattype):
    followedcount = open('data.txt').read().split()
    followedcount = followedcount[2]

    unfollowedcount = open('unfollowedcount.txt').read().split()
    unfollowedcount = unfollowedcount[0]

    lasttimes = open('latesttime.txt').read().splitlines()
    n = lasttimes[0].split()
    n = n[2]
    nn = lasttimes[1].split()
    nn = nn[2]
    if whattype == 'follow':
        if int(followedcount) < limit:
            return True
        if (time() - float(n)) > 86400:
            write_to_file('otherdata', '{}  {}'
                          .format(open('data.txt').read(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            overwrite_to_file('data', 'r+', extra='Users Followed: ')
            return True  # Returns true if 24 hours have passed since last followed people.
        return False    # Retunes false if it hasn't been 24 hours

    elif whattype == 'unfollow':
        if int(unfollowedcount) < unfollowlimit:
            return True
        if (time() - float(nn)) > 86400:
            write_to_file('unfollowedtruecount', '{}  {}'
                          .format(open('unfollowedcount.txt').read(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            overwrite_to_file('unfollowedcount', 'r+')
            return True  # Returns true if 24 hours have passed since last followed people.
        return False    # Retunes false if it hasn't been 24 hours
    else:
        return False


def overwrite_to_file(filename, mode, extra=''):
    f = open('{}.txt'.format(filename), mode)
    f.seek(0)
    f.write('{}0'.format(extra))
    f.truncate()
    f.close()


def write_to_file(filename, extra=''):
    f = open('{}.txt'.format(filename), 'a+')
    f.write('{}\n'.format(extra))
    f.close()


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

        if num1 == 0 or num2 == 0:
            return False

        num4 = num1 / num2

        if num3 < 100 or num4 > .85:
            return True
        else:
            return False
    else:
        return False


# This one finds all the @ symbols on the page to look for users to follow, then throws it into a loop
def locate_user():
    while keyboard.is_pressed('q') is not True and currFollowed <= limit:
        pyautogui.scroll(-2000)
        sleep(5)
        loc = locate_image('atsign', 0.8)
        keepitgoing(zip(*loc[::-1]))


# This guy will locate an image on the page (and way better than pyautogui does)
def locate_image(imgname, threshold, color_on=False):
    if color_on is False:
        pyautogui.screenshot('img/screenshot.png')
        img_rgb = cv2.imread('img/screenshot.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('img/{}.png'.format(imgname), 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        return loc
    else:
        pyautogui.screenshot('img/screenshot.png')
        img = cv2.imread('img/screenshot.png')
        template = cv2.imread('img/{}.png'.format(imgname))
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        return loc
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)


def keepitgoing(loc):
    for pt in loc:
        if keyboard.is_pressed('q'):
            f = open('allfollowed.txt', 'a+')
            savedata()
            f.close()
            break
        try:
            global currFollowed
            f = open('allfollowed.txt', 'a+')
            if currFollowed >= 350:
                print("Daily follow limit reached (350).\nWait 24 hours to follow more.")

                savedata()
                f.close()

                # Write the last time followed to latesttime.txt
                f = open('latesttime.txt').read().splitlines()
                f[0] = 'Last Followed: {}\n'.format(time())
                open('latesttime.txt', 'w').write(''.join(f))
                quit()

            # gets the link location so we can easily get the username
            pyautogui.moveTo(pt[0] + 10, pt[1] + 5)
            pyautogui.rightClick()
            loc = locate_image('copylinklocation', 0.8)

            if len(loc[0]) == 0:
                continue
               # pyautogui.moveTo(pt[0] + 10, pt[1] + 5)
               # pyautogui.rightClick()
               # loc = locate_image('copylinklocation', 0.8)

               # for npt in zip(*loc[::-1]):
               #     pyautogui.moveRel(150)
                #    pyautogui.click()
                #    pyautogui.scroll(-2000)
                 #   break

            for npt in zip(*loc[::-1]):
                pyautogui.moveTo(npt[0], npt[1] + 5)
                pyautogui.click()
                pyautogui.moveRel(-750)
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
            loc = locate_image('notfollowedbyanyone', 0.8)

            # if it can't find that, it looks for the "followed by" text
            if len(loc[0]) == 0:
                loc = locate_image('followedby', 0.8)

                # and if it cant find THAT, then it just breaks
                if len(loc[0]) == 0:
                    break
                loc2 = locate_image('followbtn', 0.8)
                if len(loc2[0]) == 0:
                    loc2 = locate_image('followingbtn', .8)
                for npp in zip(*loc2[::-1]):
                    pyautogui.moveTo(npp[0] - 195, npp[1] + 190)
                    break
            else:
                for npt in zip(*loc[::-1]):
                    pyautogui.moveTo(npt[0], npt[1] + 5)
                    pyautogui.moveRel(0, -25)
                    break

            pyautogui.dragRel(275, 0, duration=.3)
            pyautogui.hotkey('ctrl', 'c')
            text = pyperclip.paste()

            try:
                # If follower / following ratio is good, it'll follow them
                if FFCount(text):
                    loc = locate_image('followbtn', 0.8)
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
            sleep(1)
        except():
            pass
