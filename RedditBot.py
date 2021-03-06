from __future__ import print_function

import builtins as __builtin__
import random
import time
import traceback

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

import winsound
import smtplib



def sendEmail(subject, body):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    senderemail_id_password="Yahoo123!"
    senderemail_id="DaColorizerBot@gmail.com"
    receiveremail_id="DaColorizerBot@gmail.com"
    smtpobj.login(senderemail_id, senderemail_id_password)

    smtpobj.sendmail(senderemail_id,receiveremail_id, "Subject: "+subject+"\n\n" + body)
    print("Sent email with subject: " + subject)

picassoUrl = "https://2.bp.blogspot.com/-GT-giB-5fos/UYNL_2WNHDI/AAAAAAAAB1I/y-tvmLnf3YU/s1600/La+Muse+by+Pablo+Picasso+OSA283.jpg"
dutchGoldUrl = "https://readtiger.com/img/wkp/en/Frans_Hals,_De_magere_compagnie.jpg"
mona = "https://www.lagazzettaitaliana.com/media/k2/items/cache/82027d123e17d4dd910754888ca7e6d1_XL.jpg"
imSorryJon = "https://i.redd.it/9nhnc6ter3151.jpg"
# mona = "https://cdn.history.com/sites/2/2016/08/GettyImages-107713626-1.jpg"
artList = [picassoUrl, dutchGoldUrl, mona, imSorryJon]

debug = False
resubmit = False  # if a file exists in out with same name do not continue
skipRedirectComment = False  # leaving the redirect comment on the orginal B&W post

monaImgUrl = ""
dutchImgUrl = ""
picassoImgUrl = ""
jonImgUrl = ""

reddit = praw.Reddit('bot1')

subList = [
    "HappyTrees", "lastimages", "history"
    , "thalassophobia", "FoggyPics", "natureporn", "imsorryjon", "wwi", "WorldWar2"
    , "otr", "pics", "blackandwhite"
    , "trippinthroughtime"
    , "TravelPorn", "Outdoors", "castles", "ArchitecturePorn", "CityPorn"
    , "cinemagraphs", "AbandonedPorn", "pic"]
random.shuffle(subList)
subList[0] = "blackandwhite"
for sub in subList:

    subreddit = reddit.subreddit(sub)
    # for submission in subreddit.hot():
    # for submission in subreddit.top("week"):
    # for submission in subreddit.new(limit=10):
    for submission in subreddit.top("month"):
        try:
            print("Title: ", submission.title)
            print("Comment Url: ", " https://reddit.com" + submission.permalink)
            print("Score: ", submission.score)
            print("URL: " +
                  submission.url)
            if "Manhattan" in submission.title:
                print("---------------------------------\n")
            if "redd" not in submission.url or submission.is_self:
                print("Issue with this post. skipping")
                continue
            # Check if this item is in blacklist
            if Tools.isBlackListed(Tools.fileToStr("blackList.txt"), Tools.slugifyNoLimit(submission.permalink)):
                print("SKIP THIS BECAUSE ITS IN BLACK LIST!!!")
                continue
            print("Photo is not blacklisted")
            # Download the image
            filename = "images/out/" + Tools.slugify(submission.title) + os.path.splitext(submission.url)[1]
            if ".jp" in submission.url and not os.path.exists(filename) \
                    and not os.path.exists(filename.replace("images/out", "images/archive/out")) or resubmit:
                # If file does not exist, it is new content and we can post it!!!
                urllib.request.urlretrieve(submission.url, 'temp.jpeg')
                # Save image to a temp file, then colorize
                basewidth = 1400
                img = Image.open('temp.jpeg')

                print("Dimensions: " + str(img.size[0]) + "x" + str(img.size[1]))
                if img.size[0] > basewidth or img.size[1] > basewidth:
                    # Resize image if too large
                    print("Resizing the image from " + str(img.size[0]) + "x" + str(img.size[1]) + " to ", end='')
                    wpercent = (basewidth / float(img.size[0]))
                    hsize = int((float(img.size[1]) * float(wpercent)))
                    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                    print(str(img.size[0]) + "x" + str(img.size[1]))
                    img.save('temp.jpeg')
                isBlackAndWhite = Tools.isGreyScale(img)
                print("IS IT BLACK AND WHITE???? " + str(isBlackAndWhite))
                if not isBlackAndWhite:
                    print("Because Photo is NOT BLACK AND WHITE we are SKIPPING it")
                    # write to blackList to skip later
                    Tools.writeToFile("blackList.txt", Tools.slugifyNoLimit(submission.permalink)+"\n")
                    continue
                img.save(filename.replace("out", "in"))

                # Colorize!
                cmd = "python Colorization.py --Win 224 --Hin 224 --input temp.jpeg --output " + filename
                start = time.time()
                os.system(cmd)

                mySubreddit = reddit.subreddit("DaColorizerBot")
                myAltSubreddit = reddit.subreddit("DaColorizerBot2")

                #submission = myAltSubreddit.submit_image("resized", "temp.jpeg")

                print("Getting DeepAI Colored Image")
                deepMindColorImg = DeepAiColorize.getDeepMindImg(submission.url)
                deepMindFileName = filename.replace(".jp", "DM.jp")
                print(deepMindColorImg)
                urllib.request.urlretrieve(deepMindColorImg, deepMindFileName)

                dmImg = Image.open(deepMindFileName)

                print("Getting DeepAI Waifu2x Image ")
                dwImgFilename = filename.replace(".jp", "DW.jp")
                deepMindWaifuImg = DeepAiWaifu.getDeepMindImg(deepMindColorImg)
                print(deepMindWaifuImg)
                urllib.request.urlretrieve(deepMindWaifuImg, dwImgFilename)

                print("Getting Original B&W Waifu2x Image ")
                origImgFilename = filename.replace(".jp", "Orig.jp")
                origImg = DeepAiWaifu.getDeepMindImg(submission.url)
                print(origImg)
                urllib.request.urlretrieve(origImg, origImgFilename)

                dwImg = Image.open(dwImgFilename)

                fastStyleTransferImg = deepMindWaifuImg
                favoredUrl = ""
                for art in artList:

                    print("Getting DeepAI Fast Style Transfer Image")
                    ddImgFilename = filename.replace(".jp", "DD.jp")
                    fastStyleTransferImg = DeepAiFastStyleTransfer.getDeepMindImg(fastStyleTransferImg, art)

                    # ddImg = Image.open(filename.replace(".jp","DD.jp"))
                    dwImgFilename = filename.replace(".jp", "DW.jp")
                    fastStyleTransferImg = DeepAiWaifu.getDeepMindImg(fastStyleTransferImg)
                    print(fastStyleTransferImg)

                    if "Picasso" in art:
                        urllib.request.urlretrieve(fastStyleTransferImg, ddImgFilename.replace("DD", "DDpicasso"))
                        favoredUrl = fastStyleTransferImg
                        myAltSubmission = myAltSubreddit.submit_image(
                            ("In the Style of Picasso: \"" + submission.title + "\"")[0:280],
                            ddImgFilename.replace("DD", "DDpicasso"))
                        picassoImgUrl = myAltSubmission.url
                    elif "compag" in art:  # dutch golden age
                        urllib.request.urlretrieve(fastStyleTransferImg, ddImgFilename.replace("DD", "DDdutch"))
                        myAltSubmission = myAltSubreddit.submit_image(
                            ("In the Style of Dutch Golden Age: \"" + submission.title + "\"")[0:280],
                            ddImgFilename.replace("DD", "DDdutch"))
                        dutchImgUrl = myAltSubmission.url
                    elif "123e17d4dd91" in art:  # mona lisa
                        urllib.request.urlretrieve(fastStyleTransferImg, ddImgFilename.replace("DD", "DDmona"))
                        myAltSubmission = myAltSubreddit.submit_image(
                            ("In the Style of the Mona Lisa: \"" + submission.title + "\"")[0:280],
                            ddImgFilename.replace("DD", "DDmona"))
                        monaImgUrl = myAltSubmission.url
                    elif "hnc6t" in art:  # imSorryJohn
                        urllib.request.urlretrieve(fastStyleTransferImg, ddImgFilename.replace("DD", "DDjon"))
                        myAltSubmission = myAltSubreddit.submit_image((
                        "In the Style of the I̸͈̾m̵͈̆S̸̮͋o̸̥͗r̵̯͝r̵̯̉y̴͌͜J̸̫̅o̸͎͆ǹ̴̫: \"" + submission.title + "\"")[0:280], ddImgFilename.replace("DD", "DDjon"))
                        jonImgUrl = myAltSubmission.url
                    comment = "It took " + str(time.time() - start)[0:4] + " seconds to create this " + str(
                        dmImg.size[0]) + "x" + str(dmImg.size[1]) + " image using [Deep Learning](https://cv-tricks.com/opencv/deep-learning-image-colorization/)!\n\n[Original Image](" + submission.url + ")\n\n*[Source - " + submission.subreddit_name_prefixed + "](" + submission.shortlink + ")*"
                    myAltSubmission.reply(comment)

                dmImg = Image.open(origImgFilename)
                dwImg = Image.open(dwImgFilename)
                print("Merging these 2 images together! dim: " + str(dmImg.size) +" and " + str(dwImg.size))
                for i in range(0, 21):
                    print(str((20 - i) * 5) + ":" + str(i * 5))
                    merged = Tools.mergeImages(dmImg, dwImg, (20 - i) * 5, i * 5)
                    if i<10: prefix = "00"
                    else: prefix = "0"
                    merged.save(filename.replace(".jp", "MERGED"+prefix + str(i) + ".jp").replace("images/out", "animations/temp"))
                    merged.save(filename.replace(".jp", "MERGED0" + str(80-i) + ".jp").replace("images/out", "animations/temp"))
                print("Merging these 2 images together! dim: " + str(img.size))
                #reformat picasso
                print("Reformatting Picasso image")
                dmImg = DeepAiWaifu.getDeepMindImg(favoredUrl)
                print(dmImg)
                urllib.request.urlretrieve(dmImg, filename.replace(".jp", "DD2picasso.jp"))

                dmImg = Image.open(dwImgFilename)
                dwImg = Image.open(filename.replace(".jp", "DD2picasso.jp"))
                print("Merging these 2 images together! dim: " + str(dmImg.size) +" and " + str(dwImg.size))
                for i in range(0, 19):
                    print(str((20 - i) * 5) + ":" + str(i * 5))
                    merged = Tools.mergeImages(dmImg, dwImg, (20 - i) * 5, i * 20)
                    merged.save(filename.replace(".jp", "MERGED0" + str(i + 20) + ".jp").replace("images/out", "animations/temp"))
                    merged.save(filename.replace(".jp", "MERGED0" + str(60 - i) + ".jp").replace("images/out", "animations/temp"))

                print("Creating GIF and Posting to reddit")
                cmd = "python FrameStitcher.py"
                os.system(cmd)
                # out.gif is ready to use
                os.rename("out.gif", filename.replace(".jpg", ".gif").replace("images/","animations/"))
                try:
                    myAltSubmission = mySubreddit.submit_image(
                    ("Transition Animation: \"" + submission.title + "\"")[0:280],
                    filename.replace(".jpg", ".gif").replace("images/","animations/"))
                except:
                    print("EXCEPTION!!! trying 1 more time")
                    time.sleep(30)
                    myAltSubmission = mySubreddit.submit_image(
                        ("Transition Animated GIF: \"" + submission.title + "\"")[0:280],
                        filename.replace(".jpg", ".gif").replace("images/","animations/"))
                comment = "It took " + str(time.time() - start)[0:4] + " seconds to create this " + str(
                    dmImg.size[0]) + "x" + str(dmImg.size[1]) + " image using [Deep Learning](https://cv-tricks.com/opencv/deep-learning-image-colorization/)!\n\n[Original Image](" + submission.url + ")\n\n*[Source - " + submission.subreddit_name_prefixed + "](" + submission.shortlink + ")*"
                myAltSubmission.reply(comment)

                print("Getting CAPTION for this image! - ", end='')
                caption = DeepAiNeuralTalk.getDeepMindImg(deepMindWaifuImg)
                print(caption)

                imgToUse = dwImg
                filenameToUse = dwImgFilename
                # Post the colorized image to my subreddit
                title = "Colorized: \"" + submission.title + "\""
                mySubmission = mySubreddit.submit_image(title[0:280], dwImgFilename)
                # Post my comment linking to original B&W image
                print(dwImgFilename + " was submitted as: " + title)

                comment = "It took " + str(time.time() - start)[0:4] + " seconds to create this " + str(
                    imgToUse.size[0]) + "x" + str(imgToUse.size[
                                                      1]) + " image using [Deep Learning](https://cv-tricks.com/opencv/deep-learning-image-colorization/)!\n\n[Original Image](" + submission.url + ")\n\n*[Source - " + submission.subreddit_name_prefixed + "](" + submission.shortlink + ")*"
                mySubmission.reply(comment)
                print("I left this comment on my subreddit's post:\n\t" + comment)

                # Now leave comment on the orginal post, redirecting to my new post's reddit image url
                redirectComment = "I think this is a great photo of " + caption + " - I'm a Deep Learning bot and I colorized this image in " + str(
                    time.time() - start)[0:4] + " seconds." \
                                  + "\n\n**[Colorized Image](" + mySubmission.url + ")**" + \
                                  "\n\n[Animated GIF of Transition](" + myAltSubmission.url + ")" + \
                                  "\n\n------\n\n[Picasso Style](" + picassoImgUrl + ")" + \
                                  "\n\n[Dutch Golden Age Style](" + dutchImgUrl + ")" + \
                                  "\n\n[Mona Lisa Style](" + monaImgUrl + ")" + \
                                  "\n\n[I̸͈̾m̵͈̆S̸̮͋o̸̥͗r̵̯͝r̵̯̉y̴͌͜J̸̫̅o̸͎͆ǹ̴̫ Style](" + jonImgUrl + ")" + \
                                  "\n\nSee more at r/DaColorizerBot\n\n[Read more about Deep Learning here.](https://cv-tricks.com/opencv/deep-learning-image-colorization/)."

                # if("blackandwhite" in submission.permalink):
                # redirectComment += "\n\nThank you r\BlackAndWhite for supporting me!!"

                try:
                    if not skipRedirectComment:
                        submission.reply(redirectComment)
                    else:
                        print("skipRedirect is enabled so we will skip leaving our redirect comment")
                except RedditAPIException as e:
                    if "doing that too much" in str(e):
                        seconds = 0
                        if "second" in str(e):
                            seconds = str(e)[0: str(e).index(" second")]
                            seconds += int(seconds[seconds.rindex(" "):])
                        if "minute" in str(e):
                            tmp = str(e)[0: str(e).index(" minute")]
                            seconds += 60 * int(tmp[tmp.rindex(" "):])
                        # Add a grace period
                        seconds += 45
                        print("We have a RATE LIMIT message from reddit: \n\t" + str(e))
                        print("We need to wait for " + str(seconds) + " more seconds!")

                        while seconds > 0:
                            time.sleep(30)
                            seconds -= 30
                            print(str(seconds) + " seconds left...")
                        print("Done Waiting!")
                        # Resubmit comment on original post
                        submission.reply(redirectComment)
                if not skipRedirectComment: print(
                    "I left this redirect comment on the orginal B&W post:\n\t" + redirectComment)
                print("Comment Url: ", " https://reddit.com" + submission.permalink)

                # upvote original submission
                submission.upvote()
                #sendEmail("IMAGE SUCCESS!! Image posted to " + submission.subreddit_name_prefixed,"Took us: " + str((time.time() - start)[0:4] + " seconds!\n"+comment))
                # wait for reddit timer to refresh
                print("Sleeping for 90 seconds - you completed one FULL POST cycle")
                time.sleep(90)
            else:
                print("We alredy proceseed " + filename + "......")
                time.sleep(0.3)
        except Exception as e:
            winsound.Beep(1000, 100)
            sendEmail("ERROR WHEN PROCESSING A IMAGE: " + str(e), "\n"+traceback.format_exc())
            print("\n\n*********\n\n\n\nERROR!!!!! PROCESSING THIS!!" + str(
                e) + "\n" + traceback.format_exc() + "\n\n\n\n")


print("COMPLETED!")
