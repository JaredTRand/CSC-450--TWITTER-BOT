import json
import pyautogui
from time import sleep
import cv2
import numpy as np
import pyperclip
import keyboard
from time import time
from datetime import datetime, timedelta
from random import randint


class TwitterBot:
    # User is the data in accountdata.json, 0 for the first one, 1 for the second, etc
    def __init__(self, user):
        self.user = user
        self.data = json.loads(open("bin/accountdata.json").read())
        self.savedata = self.data
        self.data = self.data[user]

        self.name = self.data["Name"]
        self.usersfollowed = self.data["UsersFollowed"]
        self.usersunfollowed = self.data["UsersUnfollowed"]
        self.timesleft = self.data["TimesLeft"]
        self.keywords = self.data["Keywords"]
        self.credentials = self.data["Credentials"]
        self.limits = self.data["Limits"]
        self.usersfollowedtruecount = self.data["TotalUsersFollowed"]
        self.usersunfollowedtruecount = self.data["TotalUsersUnfollowed"]

        self.totalusersfollowed = json.loads(open("bin/{}/usersfollowed.json".format(self.name)).read())
        self.totalusersunfollowed = json.loads(open("bin/{}/usersunfollowed.json".format(self.name)).read())

        self.followers = json.loads(open("bin/{}/followers.json".format(self.name)).read())

    def save_followed_user_data(self, name):
        file = "bin/{}/usersfollowed.json".format(self.name)
        self.totalusersfollowed['usersfollowed'].append(name)
        with open(file, 'r+') as j:
            json.dump(self.totalusersfollowed, j, indent=4)

    def save_unfollowed_user_data(self, name):
        file = "bin/{}/usersunfollowed.json".format(self.name)
        self.totalusersunfollowed['usersunfollowed'].append(name)
        with open(file, 'r+') as j:
            json.dump(self.totalusersunfollowed, j, indent=4)

    def clean_json(self, file, fol):
        j = json.loads(open(file).read())
        count = 0
        for x in j[fol]:
            if '@' not in x:
                j[fol].pop(count)
                print(x)
            count += 1
        print(j[fol])
        print(j)

        with open(file, 'r+') as k:
            json.dump(j, k, indent=4)

    def follow(self):
        if not self.check_time('follow') or self.usersfollowed > self.limits[0]:
            print("Daily follow limit reached".format(self.limits[0]))
            print('{} Remaining.\n\n'
                  .format(str(timedelta(seconds=((float(self.timesleft[1]) + 86400) - time())))))
            self.save_all_data()
            return
        sleep(1)
        pyautogui.PAUSE = .3
        self.find_popular_hashtag()
        self.locate_user()

    def find_popular_hashtag(self, random=True):
        loc = self.locate_image('explorebtn', .8)
        for npt in zip(*loc[::-1]):
            pyautogui.moveTo(npt[0]+20, npt[1]+25)
            pyautogui.click()
            break
        sleep(2)

        '''
        loc = self.locate_image('showmorebtn', .8)
        for npt in zip(*loc[::-1]):
            pyautogui.moveTo(npt[0]+20, npt[1]+25)
            pyautogui.click()
            break
        '''

        if random:
            loc = self.locate_image('hashtag', .9)
            for npt in zip(*loc[::-1]):
                pyautogui.moveTo(npt[0] + 20, npt[1] + randint(0, 250))
                pyautogui.click()
                break
        else:
            pass

        loc = self.locate_image('latest', .8)
        for npt in zip(*loc[::-1]):
            pyautogui.moveTo(npt[0]+10, npt[1]+25)
            pyautogui.click()
            break


    def check_time(self, whattype):
        if whattype == 'follow':
            if int(self.usersfollowed) < self.limits[0]:
                return True
            if (time() - float(self.timesleft[0])) > 86400:
                self.usersfollowedtruecount.append('{}  {}'.format(self.usersfollowed, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self.usersfollowed = 0
                self.save_all_data()
                return True  # Returns true if 24 hours have passed since last followed people.
            print('\nToo many followed today, wait a while longer.')
            print('{} Remaining.\n\n'
                  .format(str(timedelta(seconds=((float(self.timesleft[0]) + 86400) - time())))))
            return False  # Retunes false if it hasn't been 24 hours

        elif whattype == 'unfollow':
            if int(self.usersunfollowed) < self.limits[1]:
                return True
            if (time() - float(self.timesleft[1])) > 86400:
                self.usersunfollowedtruecount.append('{}  {}'.format(self.usersunfollowed, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self.usersunfollowed = 0
                self.save_all_data()
                return True  # Returns true if 24 hours have passed since last followed people.
            print('\nToo many followed today, wait a while longer.')
            print('{} Remaining.\n\n'
                  .format(str(timedelta(seconds=((float(self.timesleft[1]) + 86400) - time())))))
            return False  # Retunes false if it hasn't been 24 hours
        #else:
        #   return False

    def save_all_data(self):
        self.savedata[self.user]['UsersFollowed'] = self.usersfollowed
        self.savedata[self.user]['UsersUnfollowed'] = self.usersunfollowed
        self.savedata[self.user]['TimesLeft'] = self.timesleft
        self.savedata[self.user]['TotalUsersFollowed'] = self.usersfollowedtruecount
        self.savedata[self.user]['TotalUsersUnfollowed'] = self.usersunfollowedtruecount

        with open('bin/accountdata.json', 'r+') as j:
            json.dump(self.savedata, j, indent=4)

    def FFCount(self, s):
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
                num1 += num1 + '00'
            else:
                num1 += num1 + '000'
        if 'K' in num2:
            num2.replace('K', '')
            if '.' in num2:
                num2 = num2.replace('.', '')
                num2 += num2 + '00'
            else:
                num2 += num2 + '000'
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
    def locate_user(self):
        while keyboard.is_pressed('q') is not True and self.usersfollowed <= self.limits[0]:
            pyautogui.scroll(-2000)
            sleep(5)
            loc = self.locate_image('otheratsign', .95, color_on=True)
            s = self.keepitgoing(zip(*loc[::-1]))
            if s is False:
                break

    # This guy will locate an image on the page (and way better than pyautogui does)
    def locate_image(self, imgname, threshold, color_on=False):
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

    def keepitgoing(self, loc):
        for pt in loc:
            if keyboard.is_pressed('q'):
                self.save_all_data()
                break
            try:
                if self.usersfollowed >= self.limits[0]:
                    print("Daily follow limit reached".format(self.limits[0]))
                    print('{} Remaining.\n\n'
                          .format(str(timedelta(seconds=((float(self.timesleft[1]) + 86400) - time())))))
                    self.timesleft[0] = time()
                    self.save_all_data()
                    return False

                # gets the link location so we can easily get the username
                pyautogui.moveTo(pt[0] + 10, pt[1] + 5)
                pyautogui.rightClick()
                loc = self.locate_image('copylinklocation', 0.8)

                if len(loc[0]) == 0:
                    loc = self.locate_image('tweetbutton', .8)
                    for npt in zip(*loc[::-1]):
                        pyautogui.moveTo(npt[0], npt[1]+200)
                        pyautogui.click()
                        break
                    break

                for npt in zip(*loc[::-1]):
                    pyautogui.moveTo(npt[0], npt[1] + 5)
                    pyautogui.click()
                    pyautogui.moveRel(-750)
                    break
                pyautogui.moveTo(pt[0] + 10, pt[1] + 5)
                namelink = pyperclip.paste()
                namelink = namelink.split('/')
                namelink = namelink[len(namelink) - 1]
                namelink = '@' + namelink

                if namelink in self.totalusersfollowed['usersfollowed']:
                    pyautogui.moveRel(-300)
                    break

                # Finds the text "Not followed by anyone"
                # which is typically found on the bottom of every user when the mouse hovers over their name.
                sleep(2)
                loc = self.locate_image('notfollowedbyanyone', 0.8)

                # if it can't find that, it looks for the "followed by" text
                if len(loc[0]) == 0:
                    loc = self.locate_image('followedby', 0.8)

                    # and if it cant find THAT, then it just breaks
                    if len(loc[0]) == 0:
                        break
                    loc2 = self.locate_image('followbtn', 0.8)
                    if len(loc2[0]) == 0:
                        loc2 = self.locate_image('followingbtn', .8)
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
                    if self.FFCount(text):
                        loc = self.locate_image('followbtn', 0.8)
                        if len(loc[0]) == 0:
                            break
                        for npt in zip(*loc[::-1]):
                            pyautogui.moveTo(npt[0] + 10, npt[1] + 10)
                            break
                        pyautogui.click()
                        self.usersfollowed += 1
                        self.save_followed_user_data(namelink)
                        self.save_all_data()
                        print("{} ::: Following {}".format(self.usersfollowed, namelink))
                except IndexError:
                    pyautogui.moveRel(-500)
                    break

                pyautogui.moveRel(-750, 0)
                sleep(1)
            except():
                pass

    def unfollow(self):
        if not self.check_time('unfollow') or self.usersunfollowed >= self.limits[1]:
            print("Daily unfollow limit reached".format(self.limits[1]))
            print('{} Remaining.\n\n'
                  .format(str(timedelta(seconds=((float(self.timesleft[1]) + 86400) - time())))))
            self.save_all_data()
            return
        pyautogui.PAUSE = .3
        loc = self.locate_image('profile', .8)

        for npt in zip(*loc[::-1]):
            pyautogui.moveTo(npt[0], npt[1] + 5)
            pyautogui.moveRel(+10, +15)
            pyautogui.click()
            break

        sleep(3)

        loc = self.locate_image('profilefollowers', .9)

        for npt in zip(*loc[::-1]):
            pyautogui.moveTo(npt[0], npt[1] + 5)
            pyautogui.moveRel(+5, +5)
            pyautogui.click()
            break
        self.save_followers_data()
        sleep(1)
        pyautogui.click()
        loc = self.locate_image('profilefollowing', .9)

        for npt in zip(*loc[::-1]):
            pyautogui.moveTo(npt[0], npt[1] + 5)
            pyautogui.moveRel(+5, +5)
            pyautogui.click()
            break
        sleep(2)

        pyautogui.PAUSE = .9
        for n in range(10):
            pyautogui.hotkey('end')
        pyautogui.PAUSE = .3

        while self.usersunfollowed <= 85:
            loc = self.locate_image('otheratsign', .95, color_on=True)
            s = self.dothething(loc)
            pyautogui.scroll(1750)
            sleep(1)
            if s is False:
                break

    def dothething(self, loc):
        for npt in zip(*loc[::-1]):
            if self.usersunfollowed >= self.limits[1]:
                print("Daily unfollow limit reached".format(self.limits[1]))
                print('{} Remaining.\n\n'
                      .format(str(timedelta(seconds=((float(self.timesleft[1]) + 86400) - time())))))
                self.timesleft[1] = time()
                self.save_all_data()
                return False
            pyautogui.moveTo(npt[0] - 4, npt[1] + 9)
            pyautogui.dragRel(300, 0, duration=.7)
            pyautogui.hotkey('ctrl', 'c')
            copy = pyperclip.paste()
            copy = copy.split()
            name = copy[len(copy) - 1]
            if name in self.followers['followers'] or 'Follows' in copy or name in self.totalusersunfollowed['usersunfollowed']:
                continue
            else:
                print("{} ::: Unfollowing {}".format(self.usersunfollowed, name))
                self.save_unfollowed_user_data(name)
                pyautogui.moveRel(165, -10)
                pyautogui.click()
                self.usersunfollowed += 1
                print(self.usersunfollowed)
                loc = self.locate_image('unfollowbtn', .8)

                for nptt in zip(*loc[::-1]):
                    pyautogui.moveTo(nptt[0], nptt[1] + 5)
                    pyautogui.moveRel(+20, +20)
                    pyautogui.click()
                    break
                self.save_all_data()

    def save_followers_data(self):
        pyautogui.hotkey('f5')
        sleep(2)
        loc = self.locate_image('tweetbutton', .8)

        for npt in zip(*loc[::-1]):
            pyautogui.moveTo(npt[0], npt[1] + 5)
            pyautogui.moveRel(+50, +150)
            pyautogui.click()
            break
        newfollowers = []
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        eew = str(pyperclip.paste())
        eew = eew.split()
        for c in eew:
            if c.startswith('@'):
                newfollowers.append(c)
        for i in range(15):
            pyautogui.hotkey('end')
            sleep(.5)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')
            eew = str(pyperclip.paste())
            eew = eew.split()
            for c in eew:
                if c.startswith('@'):
                    newfollowers.append(c)
            pyautogui.click()

        newfollowers = list(dict.fromkeys(newfollowers))
        self.followers['followers'] = newfollowers

        with open("bin/{}/followers.json".format(self.name), 'r+') as j:
            json.dump(self.followers, j, indent=4)

    def twitterLogin(self):
        pass

    def searchKeyword(self):
        pass

    def likeTweet(self):
        pass

    def retweet(self):
        pass

    def get_values_as_list(self):
        return [self.name, self.usersfollowed, self.usersunfollowed, self.timesleft,
                self.keywords, self.credentials]

    def get_values_as_json(self):
        return self.data
