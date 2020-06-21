import time

import praw
import pdb
import re
import os
import urllib.request
from PIL import Image


import praw
from praw.exceptions import RedditAPIException

import Tools

debug = False
resubmit = False  #if a file exists in out with same name do not continue
skipRedirectComment = True  #skip leaving the redirect comment on the orginal B&W post

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("blackandwhite")

for submission in subreddit.hot(limit=5):
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
            print("Resizing the image from " + str(img.size[0])+ "x" + str(img.size[1]) + " to ", end='')
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            print(str(img.size[0]) + "x" + str(img.size[1]))
            img.save('temp.jpeg')
            time.sleep(5)
        else: print("Image is " + str(img.size[0]) + "x" + str(img.size[1]))
        #Colorize!
        cmd = "python Colorization.py --Win 750 --Hwin 750 --input temp.jpeg --output " + filename
        start = time.time()
        os.system(cmd)
        start = time.time() - start
        #image is now saved at images/out/filename
        #submission.reply("This is a test of the new colorization Bot!")

        #Post the colorized image to my subreddit
        mySubreddit = reddit.subreddit("DaColorizerBot")
        title = "Colorized: " + submission.title
        mySubmission = mySubreddit.submit_image(title, filename)
        #Post my comment linking to original B&W image
        print(filename + " was submitted as: " + title)

        comment = "It took " + str(start)[0:4] + " seconds to colorize this " + str(img.size[0]) + "x" + str(img.size[1]) + " image using [Deep Learning](https://cv-tricks.com/opencv/deep-learning-image-colorization/)!\n\n[Original Image]("+submission.url+")\n\n*[Source](" + submission.shortlink + ")*"
        mySubmission.reply(comment)
        print("I left this comment on my subreddit's post:\n\t" + comment)

        #Now leave comment on the orginal post, redirecting to my new post's reddit image url
        redirectComment = "Hello! I'm a bot and I colorized this " +str(img.size[0]) + "x" + str(img.size[1])  +" image using [Deep Learning](https://cv-tricks.com/opencv/deep-learning-image-colorization/)." \
        + "\n\n[Colorized Image](" + mySubmission.url +")\n\nIt took me " + str(start)[0:4] + " seconds to make this image 😰"
        try:
            if not skipRedirectComment: submission.reply(redirectComment)
            else: print("skipRedirect is enabled so we will skip leaving our redirect comment")
        except RedditAPIException as e:
            if "doing that too much" in str(e):
                seconds = 0
                if "second" in str(e):
                    seconds = str(e)[0: str(e).index(" second")]
                    seconds += int(seconds[seconds.rindex(" "):])
                if "minute" in str(e):
                    tmp = str(e)[0: str(e).index(" minute")]
                    seconds += 60 * int(tmp[tmp.rindex(" "):])
            #Add a grace period just to be nice to reddit's servers
            seconds += 30
            print("We have a RATE LIMIT message from reddit: \n\t" + str(e))
            print("We need to wait for " + str(seconds-30) + " more seconds!")
            while seconds > 5 + seconds/2:
                time.sleep(6 + seconds/2)
                seconds -= 6 + seconds/2
                print(seconds + " left...")
            print("Done Waiting!")
            #Resubmit comment on original post
            submission.reply(redirectComment)
        print("I left this redirect comment on the orginal B&W post:\n\t" + redirectComment)

        #wait for reddit timer to refresh
        print("Sleeping for 30 seconds - you completed one FULL POST cycle")
        time.sleep(30)
    else:
        print("WE alredy proceseed " + filename + "......")
        time.sleep(3)

print("COMPLETED!")
