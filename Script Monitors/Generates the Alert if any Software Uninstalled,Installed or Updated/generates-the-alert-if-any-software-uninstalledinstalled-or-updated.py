import os,re,sys
import _winreg,difflib,filecmp
li=[]
def collectprograms(rtkey,pK,kA):
    import _winreg
    import os
    try:      
        oK=_winreg.OpenKey(rtkey,pK,0,kA)
        i=0
        while True:
          try:
           bkey=_winreg.EnumKey(oK,i)
           vkey=os.path.join(pK,bkey)
           oK1=_winreg.OpenKey(rtkey,vkey,0,kA)
           try:
            DN,bla=_winreg.QueryValueEx(oK1,'DisplayName')
            DV,bla=_winreg.QueryValueEx(oK1,'DisplayVersion')
            li.append([DN.strip(),DV.strip()])
           except:
            pass
           i+=1
          except:
           break
    except:
        pass
    
    _winreg.CloseKey(oK)
    return li

def programsinstalled():
 uninstallkey='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
 if 'PROGRAMFILES(X86)' in os.environ.keys():
  rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
      (_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ),
      (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
      (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ)]
 else:
  rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_READ),
      (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_READ)]

 for i in rklist:
  col=collectprograms(i[0], i[1], i[2])
 return col
k=programsinstalled()

fileToSend1=os.path.join(os.path.join(os.environ['ProgramData'],'c1_temp'),'installed1.txt')
fileToSend2=os.path.join(os.path.join(os.environ['ProgramData'],'c1_temp'),'installed2.txt')
file1=fileToSend1
file2=fileToSend2
inst_path=r"C:\ProgramData\c1_temp"
if not os.path.exists(inst_path):
    os.makedirs(inst_path)
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))


def files():
     if os.path.exists(fileToSend1):
         fnd=1
     else:
         fnd=2
     return fnd
    
def write():
    f=files()
    os.chdir(inst_path)
    if f==2:
        with open(fileToSend1, 'w+') as f:
            for i in k:
              f.write('  '.join(i).encode('utf-8')+"\n")
                    
        with open(fileToSend2, 'w+') as f:
            for i in k:
              f.write('  '.join(i).encode('utf-8')+"\n")
    if f==1:
        with open(fileToSend2, 'w+') as f:
            for i in k:
                f.write('  '.join(i).encode('utf-8')+"\n")
          
  
def compare():
 ale=0
 with open(file1) as file:
  data=file.read()
 with open(file2) as file:
  data2=file.read()
 text1Lines = data.splitlines(1)
 text2Lines = data2.splitlines(1)  
 diffInstance = difflib.Differ()
 if len(text1Lines)==len(text2Lines):
     diffList = list(diffInstance.compare(text2Lines, text1Lines))
     li=[]
     li1=[]
     for line in diffList:
         if line.startswith('+'):
             k=line.strip().strip('+')
             li.append(k)
         if line.startswith('-'):
             k1=line.strip().strip('-')
             li1.append(k1)
     if li and li1:
         ale=1
         for i in li :
             for j in li1 :
                 print i,'software has been replaced with',j
     else:
         print "No changes in Softwares at end point "
         ale=0
                  
 else:
     diffList = list(diffInstance.compare(text2Lines, text1Lines))
     for line in diffList:
      if line[0] == '-':
       print "Installed softwares are :"
       print line
       ale=1
     diffList = list(diffInstance.compare(text1Lines, text2Lines))
     for line in diffList:
      if line[0] == '-':
       print "Uninstalled softwares are :"
       print line
       ale=1
 return ale

write()
        
def remove():
    os.remove(fileToSend1)
    os.rename(fileToSend2,fileToSend1)

c=compare()

if c==1:
    alert(1)
    remove()

else:
    alert(0)
    remove()
    

