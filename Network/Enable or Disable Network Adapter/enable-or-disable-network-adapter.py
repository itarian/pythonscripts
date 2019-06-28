set_value=1    #   set_value should be 0 or 1, '0' to ENABLE '1' to DISABLE

import os
import re

print "------Getting Network adapter Details------\n"
net=os.popen("netsh interface show interface").read()
print net
n=re.findall('--\n(.*)', net)
name=''.join(n)
na=name.split('  ')[-1]
print na
if set_value==0:
    print "Choosen to Enable Network adapter\n"
    get=os.popen("netsh interface set interface "+na+" admin=enable").read()
    print "***NETWORK ENABLED SUCCESSFULLY***"

else:
    print "Choosen to Disable Network adapter\n"
    print "NOTE: Your System will lost network and automatically Disconnect\n"
    print "***NETWORK DISABLED SUCCESSFULLY***"
    get=os.popen("netsh interface set interface "+na+" admin=disable").read()
    
