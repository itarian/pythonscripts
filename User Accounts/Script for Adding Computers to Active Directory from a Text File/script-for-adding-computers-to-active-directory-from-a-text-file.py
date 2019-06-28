import os
import ctypes
import os.path
import sys
data0=[]
data0 = [line.strip() for line in open("C:/ProgramData/computers.txt", 'r')]   #provide the path where the text file is saved
print "The computers are"
print data0
for i in range (len(data0)):
            data0[i]
            cmd=r"net computer \\"+data0[i]+" /add"
            os.popen(cmd).read()
            print data0[i] + " is added"
