#Archives images files
import os
from os import listdir
from os.path import isfile, join
from sys import path
exit()
myPath = "images/out"
onlyFiles = [f for f in listdir(myPath) if isfile(join(myPath, f))]
for file in onlyFiles:
    os.rename(myPath+"/"+str(file), "images/archive/out/"+str(file))
    #f = open(myPath + "/"+str(file), "w")
    #f.close()
    print("Archived " + str(file))
