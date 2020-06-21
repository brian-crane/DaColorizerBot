import os
import time

for i in range(1,250, 5):
    print("We proessing with Hin,Win = " + str(i))
    num = "0"
    for b in range(0, 4-len(str(i))):
        num += "0"
    cmd = "python Colorization.py --Win "+str(i)+" --Hin "+str(i)+" --input temp.jpeg --output animations/test"+num+str(i)+".jpeg"
    start = time.time()
    os.system(cmd)
    start = time.time() - start
    print(str(start) + " seconds to process this")
