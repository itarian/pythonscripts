name="Themes" # provide the name of the service

a=1
#provide value for a based on following:
#set a=0 to stop service
#set a=1 to start service
#set a=2 to pause service
#set a=3 to resume service
import os
import re
print "------Listing windows services------\n"
net=os.popen("net start ").read()
print net
if (a==0):

    print"-------STOPPING A SERVICE-----\n"
    stop=os.popen("net stop "+ name ).read()
    print stop
    check=os.popen("sc query " +name).read()
    print check
    
elif (a==1):
    print"-------STARTING A SERVICE-----\n"
    start=os.popen("net start "+ name ).read()
    print start
    chec=os.popen("sc query " +name).read()
    print chec

elif(a==2):
    print"-------PAUSING A SERVICE-----\n"
    rest=os.popen("net pause "+ name ).read()
    print rest
    checka=os.popen("sc query " +name).read()
    print checka
    
elif(a==3):
    print"-------RESUMING A SERVICE-----\n"
    con=os.popen("net continue "+ name ).read()
    print con
    checken=os.popen("sc query "+name).read()
    print checken
    
else:
    print('please ser value to a')
