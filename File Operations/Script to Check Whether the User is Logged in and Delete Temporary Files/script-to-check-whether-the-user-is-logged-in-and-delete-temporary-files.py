import os
import tempfile
nam=os.environ['USERNAME']
name=os.environ['COMPUTERNAME']
print "Computer name: "+name
cmd=os.popen('query user /server:'+name).read()
if "Active" in cmd:
    print "Current User : "+nam+" is logged in. "
else:
    print "No user is logged into the system"

def deletetempfiles():
    for rt, di, fi in os.walk(tempfile.gettempdir()):
        for fn in fi:
            try:
                os.remove(os.path.join(rt, fn))
            except Exception as e:
                print e
if __name__=='__main__':
    print"Temporary Files from the Current User Directory is successfully deleted"
    deletetempfiles()

