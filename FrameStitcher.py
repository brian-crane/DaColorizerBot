import cv2
import os
from moviepy.editor import *

#From a folder of images we can create a video

image_folder = 'animations/temp'
video_name = 'out.avi'
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 10, (width,height))

count = 0
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))
    #print('.' , end='')
    if count % 100 == 0:
        print(count)
    count += 1

cv2.destroyAllWindows()
video.release()

clip = (VideoFileClip("out.avi"))

cmd = "ffmpeg -i out.avi -s "+str(height*0.7)+"x"+str(width*0.7)+" output.mp4"
os.system(cmd)


clip.write_gif("out.gif")

for f in os.listdir(image_folder):
    print("x",end='')
    os.remove("animations/temp/"+f)

print("files removed and we are DONE!")

