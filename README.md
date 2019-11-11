# TWITTER BOT
## Because I wasn't allowed to have the twitter API

To run the program, just run brain.py :)

You may have to change some things around in the bin folder and accountdata.json for it to work the way you want. You can change the name to be anything you want, but the name has to be the same as the folder, otherwise it will probably break. 


As of right now, change the code at the bottom of brain.py to do what you want. For example,


```
bot1 = TwitterBot(user=0)  <-- This creates a new bot from the first portion of accountdata.json in bin
bot1.follow()   <-- This part will follow users, just be sure the twitter page is open when you start
bot1.unfollow()   <-- This makes a list of everyone who follows it and unfollows users that don't follow the bot back
bot2 = TwitterBot(user=1)   <-- This is assuming there's another portion in the accountdata.json
swap_user(bot2)   <-- This will log out bot1 and log in bot2, just make sure the credentials are in accountdata.json
```


There's also a small bug where something adds extra brackets to accountdata.json, so just delete them if it does that. I'll try to fix that up soon

