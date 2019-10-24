import pyautogui
from time import sleep
from Follow import locate_image
import pyperclip


def unfollow():
    pyautogui.PAUSE = .3
    loc = locate_image('profile', .8)

    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0], npt[1] + 5)
        pyautogui.moveRel(+10, +15)
        pyautogui.click()
        break

    sleep(3)
    loc = locate_image('profilefollowers', .9)

    for npt in zip(*loc[::-1]):
        pyautogui.moveTo(npt[0], npt[1] + 5)
        pyautogui.moveRel(+5, +5)
        pyautogui.click()
        break

    sleep(3)
    loc = locate_image('tweetbutton', .8)

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
    loc = locate_image('profilefollowing', .9)

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
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.hotkey('end')
    pyautogui.PAUSE = .3

    f = open('unfollowedcount.txt', 'r+')
    num = f.read()
    num = int(num)
    curunfollowed = num

    while curunfollowed <= 85:
        loc = locate_image('atSign', .9)
        dothething(loc)
        pyautogui.scroll(1500)
        sleep(.5)


def dothething(loc):
    f = open('followers.txt', 'r')
    g = f.read()
    f.close()

    f = open('unfollowedcount.txt', 'r+')
    num = f.read()
    num = int(num)
    curunfollowed = num

    for npt in zip(*loc[::-1]):
        if curunfollowed >= 85:
            print('Too many unfollowed today. Edit unfollowedcount.txt to unfollow more.')
            quit()
        pyautogui.moveTo(npt[0] - 4, npt[1] + 9)
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
            print(curunfollowed)
            loc = locate_image('unfollowbtn', .8)

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

