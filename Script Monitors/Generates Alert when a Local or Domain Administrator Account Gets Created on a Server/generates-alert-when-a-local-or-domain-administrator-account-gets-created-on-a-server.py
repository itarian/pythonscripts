import os;
import ctypes
import os.path
import sys
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
    

data0=[]
if not os.path.isfile('C:/ProgramData/me.txt'):
    a = os.popen('dsquery group -name "domain admins" | dsget group -members | dsget user -display > C:/ProgramData/me.txt').read()
    data0 = [line.strip() for line in open("C:/ProgramData/me.txt", 'r')]
    print "are the default users"
    print data0
    alert(0)

else:
    b = os.popen('dsquery group -name "domain admins" | dsget group -members | dsget user -display > C:/ProgramData/we.txt').read()
    data1 = [line.strip() for line in open("C:/ProgramData/we.txt", 'r')]
    data0 = [line.strip() for line in open("C:/ProgramData/me.txt", 'r')]
    if (list(set(data1).difference (set(data0)))):
        result = list(set(data1).difference (set(data0)))
        print "new user is/are"
        print result 
        for i in range (0,len(result)):
            fh = open('C:/ProgramData/me.txt', 'a+')
            fh.write("\n" +result[i])
            fh.close()
            data0.append(result[i])
        alert(1)   
    else:
        print "no user added"
        alert(0)
