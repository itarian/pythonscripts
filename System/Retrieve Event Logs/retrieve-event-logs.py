Event_ID=0              # INTEGER
LogName= "Application"  # STRING
SourceName="CPMService" # STRING
Recent=1                # INTEGER

import subprocess
from subprocess import PIPE, Popen
cmd='powershell "Get-EventLog -LogName %s -Newest %s -Source "%s" | Where-Object {$_.EventID -eq %s} |Select-Object -Property *"' % (LogName, Recent, SourceName, Event_ID)
obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
out, err = obj.communicate()
if out:
    print out
elif "No matches found" in err:
    print "No matches found"
else:
    print err
