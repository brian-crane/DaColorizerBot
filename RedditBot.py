import random
import time

import cv2
import praw
import pdb
import re
import os
import urllib.request
from PIL import Image


import praw
from praw.exceptions import RedditAPIException

import DeepAiColorize
import DeepAiDream
import DeepAiFastStyleTransfer
import DeepAiNeuralTalk
import DeepAiWaifu
import Tools

picassoUrl = "https://2.bp.blogspot.com/-GT-giB-5fos/UYNL_2WNHDI/AAAAAAAAB1I/y-tvmLnf3YU/s1600/La+Muse+by+Pablo+Picasso+OSA283.jpg"
dutchGoldUrl = "https://readtiger.com/img/wkp/en/Frans_Hals,_De_magere_compagnie.jpg"
mona = "https://dwellingintheword.files.wordpress.com/2011/04/last-supper.jpg"
imSorryJon = "https://i.redd.it/9nhnc6ter3151.jpg"
#mona = "https://cdn.history.com/sites/2/2016/08/GettyImages-107713626-1.jpg"
artList = [picassoUrl, dutchGoldUrl, mona, imSorryJon]

debug = False
resubmit = False  #if a file exists in out with same name do not continue
skipRedirectComment = False  # leaving the redirect comment on the orginal B&W post

monaImgUrl=""
dutchImgUrl=""
picassoImgUrl=""
jonImgUrl=""

reddit = praw.Reddit('bot1')

subList = ["imsorryjon","HistoryPorn","wwi","WorldWar2"
    ,"photographs","OldSchoolCool","otr","pics","blackandwhite"
           ,"art","anime","instagram","mapporn","trippinthroughtime"
           ,"cinemagraphs","AbandonedPorn","pic"]
for sub in subList:

    subreddit = reddit.subreddit(sub)
    #for submission in subreddit.hot():
    #for submission in subreddit.top("week"):
    #for submission in subreddit.new(limit=10):

    for submission in subreddit.top("week"):
        print("Title: ", submission.title)
        print("Comment Url: ", " https://reddit.com"+submission.permalink)
        print("Score: ", submission.score)
        print("URL: " +
              submission.url )
        if "Manhattan" in submission.title:
            print("---------------------------------\n")
        if "redd" not in submission.url or submission.is_self:
            print("Issue with this post. skipping")
            continue
        #Download the image
        filename = "images/out/" + Tools.slugify(submission.title) + os.path.splitext(submission.url)[1]
        if ".jp" in submission.url and not os.path.exists(filename) or resubmit :
            #If file does not exist, it is new content and we can post it!!!
            urllib.request.urlretrieve(submission.url, 'temp.jpeg')
            #Save image to a temp file, then colorize
            basewidth = 2000
            img = Image.open('temp.jpeg')

            print("Dimensions: " + str(img.size[0]) + "x" + str(img.size[1]))
            if img.size[0] > basewidth or img.size[1] > basewidth :
                #Resize image if too large
                print("Resizing the image from " + str(img.size[0])+ "x" + str(img.size[1]) + " to ", end='')
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                print(str(img.size[0]) + "x" + str(img.size[1]))
                img.save('temp.jpeg')
            isBlackAndWhite = Tools.is_grey_scale(img)
            print("IS IT BLACK AND WHITE???? " + str(isBlackAndWhite))
            if not isBlackAndWhite :
                print("Because Photo is NOT BLACK AND WHITE we are SKIPPING it")
                continue
            img.save(filename.replace("out","in"))

            #Colorize!
            cmd = "python Colorization.py --Win 224 --Hin 224 --input temp.jpeg --output " + filename
            start = time.time()
            os.system(cmd)

            print("Getting DeepAI Colored Image")
            deepMindColorImg = DeepAiColorize.getDeepMindImg(submission.url)
            print(deepMindColorImg)
            urllib.request.urlretrieve(deepMindColorImg, filename.replace(".jp","DM.jp"))

            dmImg = Image.open(filename.replace(".jp","DM.jp"))

            print("Getting DeepAI Waifu2x Image ")
            dwImgFilename = filename.replace(".jp","DW.jp")
            deepMindWaifuImg = DeepAiWaifu.getDeepMindImg(deepMindColorImg)
            print(deepMindWaifuImg)
            urllib.request.urlretrieve(deepMindWaifuImg, dwImgFilename)

            temp = DeepAiWaifu.getDeepMindImg(submission.url)
            urllib.request.urlretrieve(temp, 'temp.jpeg')

            dwImg = Image.open(dwImgFilename)
            img = Image.open('temp.jpeg')
            #merged = Tools.mergeImages(dwImg,img, 50,50)
            #cv2.imwrite('merged.jpeg', merged)

            print("Getting CAPTION for this image!")
            caption = DeepAiNeuralTalk.getDeepMindImg(deepMindWaifuImg)


            dwImg = Image.open(dwImgFilename)
            mySubreddit = reddit.subreddit("DaColorizerBot")

            fastStyleTransferImg = deepMindWaifuImg
            for art in artList:

                print("Getting DeepAI Fast Style Transfer Image")
                ddImgFilename = filename.replace(".jp","DD.jp")
                fastStyleTransferImg = DeepAiFastStyleTransfer.getDeepMindImg(fastStyleTransferImg, art)

                #ddImg = Image.open(filename.replace(".jp","DD.jp"))
                dwImgFilename = filename.replace(".jp","DW.jp")

                fastStyleTransferImg = DeepAiWaifu.getDeepMindImg(fastStyleTransferImg)
                print(fastStyleTransferImg)

                if "Picasso" in art:
                    urllib.request.urlretrieve(fastStyleTransferImg, ddImgFilename.replace("DD","DDpicasso"))
                    myAltSubmission = mySubreddit.submit_image(("In the Style of Picasso: \"" + submission.title +"\"")[0:280], ddImgFilename.replace("DD","DDpicasso"))
                    picassoImgUrl = myAltSubmission.url
                elif "compag" in art: #dutch golden age
                    urllib.request.urlretrieve(fastStyleTransferImg, ddImgFilename.replace("DD","DDdutch"))
                    myAltSubmission = mySubreddit.submit_image(("In the Style of Dutch Golden Age: \"" + submission.title +"\"")[0:280], ddImgFilename.replace("DD","DDdutch"))
                    dutchImgUrl = myAltSubmission.url
                elif "llinginth" in art: #mona lisa
                    urllib.request.urlretrieve(fastStyleTransferImg, ddImgFilename.replace("DD","DDmona"))
                    myAltSubmission = mySubreddit.submit_image(("In the Style of the Mona Lisa: \"" + submission.title +"\"")[0:280], ddImgFilename.replace("DD","DDmona"))
                    monaImgUrl = myAltSubmission.url
                elif "hnc6t" in art: #imSorryJohn
                    urllib.request.urlretrieve(fastStyleTransferImg, ddImgFilename.replace("DD","DDjon"))
                    myAltSubmission = mySubreddit.submit_image(("In the Style of the I̸͈̾m̵͈̆S̸̮͋o̸̥͗r̵̯͝r̵̯̉y̴͌͜J̸̫̅o̸͎͆ǹ̴̫: \"" + submission.title +"\"")[0:280], ddImgFilename.replace("DD","DDjon"))
                    jonImgUrl = myAltSubmission.url
                comment = "It took " + str(time.time() - start)[0:4] + " seconds to create this " + str(dmImg.size[0]) + "x" + str(dmImg.size[1]) + " image using [Deep Learning](https://cv-tricks.com/opencv/deep-learning-image-colorization/)!\n\n[Original Image]("+submission.url+")\n\n*[Source - "+submission.subreddit_name_prefixed+"](" + submission.shortlink + ")*"
                myAltSubmission.reply(comment)

            imgToUse = dwImg
            filenameToUse = dwImgFilename
            #Post the colorized image to my subreddit
            title = "Colorized: \"" + submission.title +"\""
            mySubmission = mySubreddit.submit_image(title[0:280], dwImgFilename)
            #Post my comment linking to original B&W image
            print(dwImgFilename + " was submitted as: " + title)

            comment = "It took " + str(time.time() - start)[0:4] + " seconds to create this " + str(imgToUse.size[0]) + "x" + str(imgToUse.size[1]) + " image using [Deep Learning](https://cv-tricks.com/opencv/deep-learning-image-colorization/)!\n\n[Original Image]("+submission.url+")\n\n*[Source - "+submission.subreddit_name_prefixed+"](" + submission.shortlink + ")*"
            mySubmission.reply(comment)
            print("I left this comment on my subreddit's post:\n\t" + comment)

            #Now leave comment on the orginal post, redirecting to my new post's reddit image url
            redirectComment = "I think this is a great B&W photo of " + caption +" - I'm a Deep Learning bot and I colorized this image in " +str(start)[0:4] + " seconds." \
                + "\n\n**[Colorized Image](" + mySubmission.url +")**"+ \
                "\n\n------\n\n[Picasso Style](" + picassoImgUrl +")"+ \
                "\n\n[Dutch Golden Age Style](" + dutchImgUrl +")"+ \
                "\n\n[Mona Lisa Style](" + monaImgUrl +")"+ \
                "\n\n[I̸͈̾m̵͈̆S̸̮͋o̸̥͗r̵̯͝r̵̯̉y̴͌͜J̸̫̅o̸͎͆ǹ̴̫ Style](" + jonImgUrl +")"+ \
                "\n\nSee more at r/DaColorizerBot\n\n[Read more about Deep Learning here.](https://cv-tricks.com/opencv/deep-learning-image-colorization/)."


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
                    #Add a grace period
                    seconds += 45
                    print("We have a RATE LIMIT message from reddit: \n\t" + str(e))
                    print("We need to wait for " + str(seconds) + " more seconds!")

                    while seconds > 0:
                        time.sleep(30)
                        seconds -= 30
                        print(str(seconds) + " seconds left...")
                    print("Done Waiting!")
                    #Resubmit comment on original post
                    submission.reply(redirectComment)
            if not skipRedirectComment: print("I left this redirect comment on the orginal B&W post:\n\t" + redirectComment)
            print("Comment Url: ", " https://reddit.com"+submission.permalink)

            #upvote original submission
            submission.upvote()

            #wait for reddit timer to refresh
            print("Sleeping for 15 seconds - you completed one FULL POST cycle")
            time.sleep(15)
        else:
            print("We alredy proceseed " + filename + "......")
            time.sleep(0.3)


print("COMPLETED!")
