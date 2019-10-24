# Another Twitter Bot 

# Run brain.py to start the bot

I made this because twitter didn't "technically" give me access to a bot account, so I had to MacGyver it a little.

You need:

- Numpy

- Pyperclip

- Pyautogui

- Keyboard

- CV2

# The follow method was intended to work on trending tweets sorted by "latest"

Technically it could work anywhere, but It works best on those fresh out of the oven tweets.

The bot will look for the @ symbol relating to users twitter handles (And, oh my god, can I say how much better CV2 works than pyautogui for finding images on screen? It's like night and day!). It will hover over the symbol and see if their follower/following count is a sufficient ratio to follow them.

The pictures might be different than whats on your screen, same with the amount of pixels the mouse moves, so you might have to change them to fit your system. This definitely isn't the best method, but it works okay for now. I think that in the future, using a combination of CV2's image finding and a browser engine like selenium would yield the best results.

Sometimes it still wigs out a little bit, so keep an eye on it to make sure it doesn't do anything weird.


My next step after making sure that it can follow/unfollow without goofing is to automate it more. As in, I intend to have it follow and unfollow people every day without me needing to press the buttons to start it up. 

Ooh, and I want it to keep track of how many people it follows in a day by itself. As of right now I have to change the txt files manually, and boy does that get annoying. I might whip that up in the next few days.

Maybe eventually I could get it to tweet by itself too.
