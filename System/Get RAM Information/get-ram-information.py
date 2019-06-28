import os
print "PC Name : "+os.environ['COMPUTERNAME']
print os.popen('systeminfo | findstr /c:"Total Physical Memory" /c:"Available Physical Memory"').read()
