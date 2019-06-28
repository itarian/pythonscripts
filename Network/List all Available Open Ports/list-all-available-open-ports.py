import os
print "\nCHECKING THE AVAILABLE PORTS:\n"
cmd=os.popen("netstat -o -n -a").read()
print cmd
