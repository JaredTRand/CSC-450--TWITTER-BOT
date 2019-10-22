import Follow
import UnFollow


if __name__ == '__main__':
    while True:
        n = int(input('What would you like me to do? \n   1. Follow Users \n   2. Unfollow Users \n   3. \n   4. Quit'))

        if n == 1:
            print("Okay, looking for users to follow.")
            Follow.follow()
            print("Finished following.")
        elif n == 2:
            print("Okay, looking for users to unfollow.")
            UnFollow.unfollow()
            print("Finished unfollowing.")
        elif n == 3:
            print('Whatever is going to be here, I have not learned how to do, either.')
        elif n == 4:
            print('Aw, okay. Bye!')
            quit()
        else:
            print('I am not sure what that means')




