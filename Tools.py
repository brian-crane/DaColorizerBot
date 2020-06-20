import os

from PIL.Image import Image


def slugify(value):
  for str in [" ",".","\"","-"]:
    value = value.replace(str,"")
  return value[0:20]

def convertToJpeg(img):
  im = Image.open("Ba_b_do8mag_c6_big.png")
  rgb_im = im.convert('RGB')
  rgb_im.save('colors.jpg')
  os.remove(img)