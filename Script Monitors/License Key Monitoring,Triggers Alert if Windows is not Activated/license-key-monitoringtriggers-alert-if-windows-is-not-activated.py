import _winreg 
import os
import re
import socket
import sys

def alert(arg):
  sys.stderr.write("%d%d%d" % (arg, arg, arg))
def information():
  name=os.environ['username']
  print 'PC-NAME : '+name
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
   
  print "IP-ADDRESS : " + (s.getsockname()[0])
  path="c:\windows\system32"
  os.chdir(path)
  out=os.popen("cscript slmgr.vbs -dli").read()
  c=0
  os.environ
  k,li,up,no,no1=[],[],[],[],[]
   
  ab=re.findall('Licensed',out)
  bc=re.findall('([0-9]{2}\sday.*)',out)
  cd=re.findall('0xC004F056',out)
  de=re.findall('0xC004F034',out)
  lea=len(ab)
  leb=len(bc)
  lec=len(cd)
  led=len(de)
  for i in ab:
      li.append(i)
  for j in bc:
      up.append(j)
  for k in cd:
      no.append(k)
  for l in de:
      no1.append(l)
  if  lea!=0:
      if ab==li:
          print "Your windows is Activated."
          alert(0)
  if leb!=0:
      if bc==up:
          up.append('Left to expire your windows,Please Activate it.')
          str1=''.join(str(e)for e in up)
          print str1
          alert(1)
  if lec!=0:
      if cd==no:
          print "You need to Activate your windows."
          alert(1)
  if led!=0:
      if de==no1:
          print "you need to Activate your windows."
          alert(1)

information()
