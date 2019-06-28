share_user=r"\\WINPRO_64-PC\share_folder" #Provide the network share path
Share_user1=r"xxxxxx" # Provide the username for the network share
share_pass="EeVeowo4" # Provide the password for network share

import os, time,ast
import sys,getpass,socket
import filecmp
old_file=os.environ['PROGRAMDATA']+r"\old_file.txt"

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
	
def oldfile(old_file,path_to_watch):
    if not os.path.exists(old_file):
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        before=str(before)
        f=open(old_file,"w")
        f.write(before)
        f.close()
        before=ast.literal_eval(before)
    else:
        f=open(old_file,"r")
        before=f.read()
        before=ast.literal_eval(before)
    return before

    
def check(share_user,old_file):    
    path_to_watch = share_user
    before=oldfile(old_file,path_to_watch) 
    if os.path.exists(old_file) :
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            print "File has Added: ", ", ".join (added)
            os.remove(old_file)
            return 1
        elif removed:
            print "File has Removed: ", ", ".join (removed)
            os.remove(old_file)
            return 1

    before = after

print "USER NAME: "+getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : "+(s.getsockname()[0])

AS=r'net use '+share_user+r' /user:'+Share_user1+r' '+share_pass+r' /P:No'
print os.popen(AS).read()

log=check(share_user,old_file)

ale=0

if log==0:
    print'check again...'
    ale=ale+1
    

elif log==1:
    print 'Changes in file'
    oldfile(old_file,share_user)
    ale=ale+1

else:
    print "No Files deleted or Added"
    ale=0
    
if ale>0:
    alert(1)
else:
    alert(0)

