from subprocess import Popen, PIPE, STDOUT
import time,os
p = Popen(['cmd.exe'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
grep_stdout = p.communicate(input=b'sc stop mms\nsc.exe config "mms" obj= ".\LocalSystem" password= ""\n')[0]
time.sleep(10)
p = Popen(['cmd.exe'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
grep_stdout = p.communicate(input=b'sc stop mms\nsc start mms\n')[0]
e=os.environ['SYSTEMDRIVE']
path=e+r"\Program Files\BackupClient\CommandLineTool\acrocmd.exe"
p = Popen(['cmd.exe'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
firewall = p.communicate(input=b'netsh advfirewall firewall add rule name="Acronis" dir=in action=allow program="%s" enable=yes\n'%(path))[0]
print "Acronis Service configured Successfully"
