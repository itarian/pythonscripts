import subprocess;
sysdown=subprocess.Popen(('shutdown /r '),shell=True,stdout=subprocess.PIPE);
for line in iter(sysdown.stdout.readline,''):
    print line.rstrip();
