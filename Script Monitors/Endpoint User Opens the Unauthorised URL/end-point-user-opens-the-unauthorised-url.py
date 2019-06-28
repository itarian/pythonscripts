global websites
websites=("www.quora.com","www.youtube.com","www.ebay.com","www.facebook.com")#Add your websites here
import os
import re
import socket
import getpass
import sys
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
def url():
    name=os.environ['username']
    print 'PC-NAME : '+name
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    print "IP-ADDRESS : " + (s.getsockname()[0])
    
    print "You are checking "+str(len(websites))+" Websites"
    c=0
    for i in websites:
        url='ipconfig /displaydns |find "'+i+'"'
        output=os.popen(url).read()
        for i  in range(0,len(websites)):
            if websites[i] in output:
                print websites[i]+" Has opened by " +name+ " user"
                c=c+1

    if c>=1:
        alert(1)
    else:
        alert(0)




url()
