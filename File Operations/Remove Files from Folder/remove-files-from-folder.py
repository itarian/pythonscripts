dirPath = r"C:\ProgramData"# provide the file path
f1="abc.exe,xyz.zip,new.txt,123.txt"# provide the file name along with its format
import os
import subprocess
f2=f1.split(",")
fileList = os.listdir(dirPath)

try:
    os.chmod(dirPath,0644)
except:
    pass
fileList = os.listdir(dirPath)

for f in fileList:
    if f in f2:
        os.chmod(dirPath,0644)
        #print dirPath
        os.remove(dirPath+"\\"+f)
    

for i in f2:
    f3=dirPath+"\\"+i
    if os.path.isfile(f3):
        print f3+ "File not removed..."
    else:
        print f3+" File removed..."
