import os
import re

networkInformation = os.popen("ipconfig /all").read()

networkInterfaces = re.findall('Description . . . . . . . . . . . :(.*)', networkInformation)
physicalAddresses = re.findall('Physical Address. . . . . . . . . :(.*)', networkInformation)

count = len(networkInterfaces)

print "Mac Address(-es) of " + os.environ['COMPUTERNAME']

for index, interface in enumerate(networkInterfaces):
    print interface + ":" + physicalAddresses[index]
