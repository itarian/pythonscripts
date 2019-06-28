import os
from math import log
def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)

drive=os.environ['SystemDrive']
fin1=os.path.join(drive,os.sep,"ProgramData","Comodo","cis")
if os.path.exists(fin1):
    fin=os.path.join(drive,os.sep,"ProgramData","Comodo")
    if os.path.exists(fin):
        f=[]
        g=[]
        s=[]
        sa=[]
        siz=[]
        os.chdir(fin)
        c=os.popen('dir /a /s /b').read()
        f=c.split('\n')
        for i in f:
            if not (i.startswith('C:\\ProgramData\\Comodo\\Installer')or  i.startswith('C:\\ProgramData\\Comodo\\Comodo ITSM\\CIS_x64.msi')):
                sa.append(i)
        def passing(l):
            if os.path.isfile(l):
                s.append(l)
            else:
                g.append(l)
                
        for i in range(0,len(sa)):
            passing(sa[i])
        
        for j in range(0,len(s)):
            s[j]+'--------- '+str(os.stat(s[j]).st_size)
            siz.append(int((os.stat(s[j]).st_size)))
        t=sorted(siz, reverse=True)[:3]
        print 'Files having largest size in CCS.....'
        for w in range(0,len(t)):
            print s[siz.index(t[w])]+'---'+str((pretty_size(t[w]))).replace('i','')
else:
    print 'COMODO CLIENT SECUITY DOESNT EXISTS IN YOUR SYSTEM...!'+'\n'
print '\n'
c=0
if os.path.exists(os.path.join(drive,os.sep,"Program Files","Comodo","Comodo ITSM")):
    ccc=os.path.join(drive,os.sep,"Program Files","Comodo","Comodo ITSM")
    c=c+1
elif os.path.exists(os.path.join(drive,os.sep,"Program Files (x86)","Comodo","Comodo ITSM")):
    ccc=os.path.join(drive,os.sep,"Program Files (x86)","Comodo","Comodo ITSM")
    c=c+1

siz_files=[]
p_list=[]
p_list1=[]
p_list2=[]
rmm_path=os.path.join(ccc+'\\'+'rmmlogs')
pm_path=os.path.join(ccc+'\\'+'pmlogs')
spm_path=os.path.join(ccc+'\\'+'spmlogs')
ka=[]
p_list.append(rmm_path)
p_list1.append(pm_path)
p_list2.append(spm_path)
for i in p_list:
    for j in os.listdir(i):
        ka.append(os.path.join(i,j))
        os.path.join(i,j)+'--------'+str((int(os.path.getsize(os.path.join(i,j)))))
        siz_files.append((int(os.path.getsize(os.path.join(i,j)))))
        y=sorted(siz_files, reverse=True)[:3]
print 'Files having largest size in RMM'
for x in range(0,len(y)):
    print ka[siz_files.index(y[x])]+'-----'+str(pretty_size(y[x])).replace('i','')
print '\n'
for i in p_list1:
    for j in os.listdir(i):
        ka.append(os.path.join(i,j))
        os.path.join(i,j)+'--------'+str((int(os.path.getsize(os.path.join(i,j)))))
        siz_files.append((int(os.path.getsize(os.path.join(i,j)))))
        y=sorted(siz_files, reverse=True)[:3]
print 'Files having largest size in PM'
for x in range(0,len(y)):
    print ka[siz_files.index(y[x])]+'-----'+str(pretty_size(y[x])).replace('i','')
print '\n'   
for i in p_list2:
    for j in os.listdir(i):
        ka.append(os.path.join(i,j))
        os.path.join(i,j)+'--------'+str((int(os.path.getsize(os.path.join(i,j)))))
        siz_files.append((int(os.path.getsize(os.path.join(i,j)))))
        y=sorted(siz_files, reverse=True)[:3]
print 'Files having largest size in SPM'
for x in range(0,len(y)):
    print ka[siz_files.index(y[x])]+'-----'+str(pretty_size(y[x])).replace('i','')  
else:
    if c==0:
        print 'COMODO CLIENT COMMMUNICATION IS NOT PRESENT IN YOUR SYSTEM..!'
