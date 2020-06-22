import math
import os
import random
import re

import PIL
import cv2
import numpy
import numpy as np
from PIL.Image import Image

def writeToFile(filename, str):
    with open(filename, 'a') as file:
        file.write(str)
    file.close

def fileToStr(filename):
    file = open(filename, "r")
    data = file.read()
    file.close()
    return data

def isBlackListed(bL, str):
    if bL.find(str) != -1: return True
    return False

def slugify(str):
    str = str.replace(" ", "")
    out = ""
    pattern = re.compile("[a-zA-Z0-9]")
    for i in range(0, len(str) - 1):
        if pattern.match(str[i:i + 1]):
            out += str[i:i + 1]
    if len(out) == 0: out = "as" + random.randint(1, 2222)
    return out[0:20]


def convertToJpeg(img):
    im = Image.open("Ba_b_do8mag_c6_big.png")
    rgb_im = im.convert('RGB')
    rgb_im.save('colors.jpg')
    os.remove(img)

def isGreyScale2(img):
    data = numpy.asarray(img)
    pixels = list(img.getdata())
    width, height = img.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]


def isGreyScale(img):
    limit = 3
    size = img.size[0] * img.size[1]
    good = size
    img = img.convert('RGB')
    w, h = img.size
    progress = 0
    #data = numpy.asarray(img)
    for i in range(w):
        if i % (w / 10) == 0:
            print("*"+str(progress),end='')
            progress += 1
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            #r, g, b = data[j][i]
            if abs(r - g) > limit and abs(g - b) > limit and abs(r - b) > limit:
                good -= 1
                if good < size * 0.98:
                    return False
    return True


def mergeImages(img1, img2, w1, w2):
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    w, h = img1.size
    img3 = PIL.Image.new(mode = "RGB", size = (w, h))
    for i in range(w):
        if i % 100 == 0: print(".",end='')
        for j in range(h):
            r1, g1, b1 = img1.getpixel((i, j))
            r2, g2, b2 = img2.getpixel((i, j))
            newR = int(((r1 * w1 + r2 * w2) / 100))
            newG = int(((g1 * w1 + g2 * w2) / 100))
            newB = int(((b1 * w1 + b2 * w2) / 100))
            img3.putpixel((i, j), (newR, newG, newB, 255))
    return img3
