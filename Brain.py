import Follow
import UnFollow
import TwitterBot
from Follow import check_time
from time import time
from datetime import timedelta

if __name__ == '__main__':
    while True:
        n = int(input('What would you like me to do? \n   1. Follow Users \n   2. Unfollow Users'
                      ' \n   3. Try Selenium\n   4. Check Timers\n 5. Quit \n'))

        if n == 1:
            if check_time('follow') is False:
                print('\nToo many followed today, wait a while longer.')
                f = open('latesttime.txt').read().splitlines()
                f = f[0].split()
                print('{} Remaining.\n\n'
                      .format(str(timedelta(seconds=((float(f[2]) + 86400) - time())))))
                continue
            print("Okay, looking for users to follow.")
            Follow.follow()
            print("Finished following.")

        elif n == 2:
            if check_time('unfollow') is False:
                print('\nToo many unfollowed today, wait a while longer.')
                f = open('latesttime.txt').read().splitlines()
                f = f[1].split()
                print('{} Remaining.\n\n'
                      .format(str(timedelta(seconds=((float(f[2]) + 86400) - time())))))
                continue
            print("Okay, looking for users to unfollow.")
            UnFollow.unfollow()
            print("Finished unfollowing.")
        elif n == 3:
            print('This stuff is DEFINITELY still a WIP, so dont get too mad.')
            TwitterRobot = TwitterBot.TwitterBoot()
            TwitterRobot.searchKeyword()
        elif n == 4:
            f = open('latesttime.txt').read().splitlines()
            f = f[0].split()
            print('{} Remaining To Follow Again.'
                  .format(str(timedelta(seconds=((float(f[2]) + 86400) - time())))))

            f = open('latesttime.txt').read().splitlines()
            f = f[1].split()
            print('{} Remaining To Unfollow Again.\n\n'
                  .format(str(timedelta(seconds=((float(f[2]) + 86400) - time())))))
        elif n == 5:
            print('Aw, okay. Bye!')
            quit()
        else:
            print('I am not sure what that means')




