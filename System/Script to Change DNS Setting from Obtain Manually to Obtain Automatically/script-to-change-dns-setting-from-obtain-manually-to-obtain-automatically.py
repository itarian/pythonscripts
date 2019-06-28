import os
import re

intr=os.popen("wmic nic get NetConnectionid" ).read()
Name=[i.strip() for i in  intr.split("\n") if i.strip()]
a=Name[1:][-1]
print a
addr='netsh interface ipv4 show addresses "%s"'%a
addr1=os.popen(addr).read()

n=re.search("DHCP enabled:                         Yes",addr1)

if n:
    print('IP address is already configured as automatic only')
    
else:
    print("-----------CHANGING IP ADDRESS FROM MANUAL TO AUTOMATIC-------")
    
    add=os.popen('netsh interface ip set address "%s" dhcp'%a).read()
    print add
    
    addres=os.popen('netsh interface ipv4 show addresses "%s"'%a).read()
    print addres
    print("Now the ip address has changed from manual to automatic")

