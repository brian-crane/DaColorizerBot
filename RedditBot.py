import time

import praw
import pdb
import re
import os
import urllib.request
from PIL import Image


import praw

import Tools

debug = False
resubmit = True

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("blackandwhite")

for submission in subreddit.hot(limit=1):
    print("Title: ", submission.title)
    print("Score: ", submission.score)
    print("---------------------------------\n")
    #Download the image
    filename = "images/out/" + Tools.slugify(submission.title) + os.path.splitext(submission.url)[1]
    if not os.path.exists(filename) or resubmit:
        #If file does not exist, it is new content and we can post it!!!
        urllib.request.urlretrieve(submission.url, 'temp.jpeg')
        #Save image to a temp file, then colorize
        basewidth = 2500
        img = Image.open('temp.jpeg')
        if img.size[0] > 2500 or img.size[1] > 2500 :
            #Resize image if too large
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            img.save('temp.jpeg')
        #Colorize!
        cmd = "python Colorization.py --input temp.jpeg --output " + filename
        os.system(cmd)

        #image is now saved at images/out/filename
        #submission.reply("This is a test of the new colorization Bot!")

        #Post the colorized image to my subreddit
        mySubreddit = reddit.subreddit("DaColorizerBot")
        title = "Colorized: " + submission.title + " - u/" + submission.author.name
        mySubmission = mySubreddit.submit_image(title, filename)
        #Post my comment linking to original B&W image
        print(filename + " was submitted as: " + title)

        #wait for reddit timer to refresh
        print("Sleeping for 30 seconds")
        time.sleep(30)
    else:
        print("WE alredy proceseed " + filename + "......")

print("COMPLETED!")
