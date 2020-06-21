import math
import os
import re

from PIL.Image import Image

def slugify(str):
  str = str.replace(" ","")
  out = ""
  pattern = re.compile("[a-zA-Z0-9]")
  for i in range(0,len(str)-1):
    if pattern.match(str[i:i+1]):
      out += str[i:i+1]
  return out[0:20]

def convertToJpeg(img):
  im = Image.open("Ba_b_do8mag_c6_big.png")
  rgb_im = im.convert('RGB')
  rgb_im.save('colors.jpg')
  os.remove(img)

def is_grey_scale(img):
  img = img.convert('RGB')
  w,h = img.size
  for i in range(w):
    for j in range(h):
      r,g,b = img.getpixel((i,j))
      if r != g != b: return False
  return True

def mergeImages(img1, img2):
  img1 = img1.convert('RGB')
  img2 = img2.convert('RGB')
  img3 = img1
  w,h = img1.size
  for i in range(w):
    for j in range(h):
      r,g,b = img1.getpixel((i,j))
      r2,g2,b2 = img2.getpixel((i,j))
      img3.putpixel((i,j), (((r+r2)/2),((g+g2)/2),((b+b2)/2)))