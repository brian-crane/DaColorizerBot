import math
import os
import random
import re

import cv2
from PIL.Image import Image


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


def is_grey_scale(img):
    limit = 4
    size = img.size[0] * img.size[1]
    good = size
    img = img.convert('RGB')
    w, h = img.size
    progress = 0
    for i in range(w):
        if i % (w / 10) == 0:
            print("*"+str(progress),end='')
            progress += 1
        for j in range(h):
            r, g, b = img.getpixel((i, j))

            if abs(r - g) > limit and abs(g - b) > limit and abs(r - b) > limit:
                good -= 1
                if good < size * 0.95:
                    return False
    return True


def mergeImages(img1, img2, w1, w2):
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    img3 = img1
    w, h = img1.size
    for i in range(w):
        for j in range(h):
            r1, g1, b1 = img1.getpixel((i, j))
            r2, g2, b2 = img2.getpixel((i, j))
            newR = int(((r1 * w1 + r2 * w2) / 100))
            newG = int(((g1 * w1 + g2 * w2) / 100))
            newB = int(((b1 * w1 + b2 * w2) / 100))
            img3.putpixel((i, j), (newR, newG, newB, 255))
    return img3
