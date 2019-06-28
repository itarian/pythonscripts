group="abcd"           #Provide the group name"
import os
import ctypes
import os.path
import sys

data0=[]
cmd1="dsquery group -name "+group+" | dsget group -members | dsquery user -disabled | dsget user -display  > C:/ProgramData/disabled.txt"
a = os.popen(cmd1).read()
data0 = [line.strip() for line in open("C:/ProgramData/disabled.txt", 'r')]
if range (3,(len(data0)-1)):
    for i in range (3,(len(data0)-1)):
        print "The below are the disabled users"
        
        x = data0[i]
        print x
        if x:
            print "yyy"
            cmd="net user "+x+" /delete"
            os.popen(cmd).read()
else:
    print "There are no disabled users in the specified group"
