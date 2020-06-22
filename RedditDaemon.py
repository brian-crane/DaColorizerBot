import os
import time

while True:
    cmd = "python RedditBot.py"
    os.system(cmd)
    seconds = 60*60
    while seconds>60:
        seconds -= 60
        time.sleep(60)
        print(str(seconds) + " daemon seconds left")