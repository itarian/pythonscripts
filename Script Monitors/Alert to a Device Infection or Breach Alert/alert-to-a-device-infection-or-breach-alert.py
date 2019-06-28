import os
import re
import filecmp
import difflib
import sys
import sqlite3

workdir=os.environ['PROGRAMDATA']+r'\c1_temp'
if not os.path.exists(workdir):
    os.makedirs(workdir)
save_path=workdir

si1=[]
si2=[]

doll1=''
doll2=''

flag=0
global fnd,fnd3,fnd2
fnd=0
fnd2=0
fnd3=0 
global fnd1,fnd13,fnd12
fnd1=0
fnd13=0
fnd12=0
ot=save_path+"\\Output.txt"

conn = sqlite3.connect('C:\ProgramData\Comodo\Firewall Pro\cislogs.sdb')
cur1 = conn.cursor()
cur2 = conn.cursor()
cur1.execute("SELECT Path FROM AvEvents where Action=2")
cur2.execute("SELECT Path FROM AvEvents where Action=1")
rows1 = cur1.fetchall()
rows2 = cur2.fetchall()
for j in rows1:
    si1.append(j)
for k in rows2:
    si2.append(k)
def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 


def files():
 
 file_name1 = "Block_Appold.txt"
 cur_dir1 = save_path
 file_list1 = os.listdir(cur_dir1)
 parent_dir1 = os.path.dirname(cur_dir1)
 file_name2 = "remove_Appold.txt"
 cur_dir2 = save_path
 file_list2 = os.listdir(cur_dir2)
 parent_dir2 = os.path.dirname(cur_dir2)
 
 if file_name1 in file_list1:
     fnd2=1
     with open(os.path.join(save_path, "Block_Appnew"+".txt"), "w") as file21:
         for j in si1:
             j=str(j)
             u =j.split("u'")[1]
             v =u.split("',)")[0]
             if 'Service' in v:
                 pass
             else:
                 file21.write(v+'\n')
                 fnd2=1      
 if file_name2 in file_list2:
     fnd3=1
     with open(os.path.join(save_path, "remove_Appnew"+".txt"), "w") as file22:
         for k in si2:
             k=str(k)
             e =k.split("u'")[1]
             f =e.split("',)")[0]
             if 'Service' in f:
                 pass
             else:
                 file22.write(f+'\n')
                 fnd3=1      

 else:
     fnd2=2
     fnd3=2
 return fnd2
 return fnd3


def swchanges():
    
    file11=save_path+"\\Block_Appnew.txt"
    file21=save_path+"\\Block_Appold.txt"
    file12=save_path+"\\remove_Appnew.txt"
    file22=save_path+"\\remove_Appold.txt"
    ot=save_path+"\\Output.txt"
    flag=0
  
    if False==0:
        
        with open(file11) as file:
           data1=file.read()
           data1.strip()
           with open(file21) as file:
               data21=file.read()
               data21.strip()
               text1Lines1 = data1.splitlines(1)
               text2Lines1 = data21.splitlines(1)
               diffInstance1 = difflib.Differ()
               diffList1 = list(diffInstance1.compare(text1Lines1,text2Lines1 ))
               with open(ot, 'a+') as o1:
                   o1.write("\n********** Blocked Application***********\n")
                   for line in diffList1:
                       if line[0] == '-':
                           flag=1
                           o1.write("File has Added  "+line)
               o1.close()  
           file.close()
        file.close()            
         
    if False==0:
        
        with open(file12) as file:
           data2=file.read()
           data2.strip()
           with open(file22) as file:
               data22=file.read()
               data22.strip()
               text1Lines2 = data2.splitlines(1)
               text2Lines2 = data22.splitlines(1)
               diffInstance2 = difflib.Differ()
               diffList2 = list(diffInstance2.compare(text1Lines2,text2Lines2 ))
               with open(ot, 'a+') as o1:
                   o1.write("\n********** Removed Application ***********\n")
                   for line in diffList2:
                       if line[0] == '-':
                           flag=1
                           o1.write("File has Added  "+line)
               o1.close()  
           file.close()
        file.close()           
               
        return flag 


def remove():
    
    os.remove(save_path+"\\Block_Appold.txt")
    os.rename(save_path+"\\Block_Appnew.txt",save_path+"\\Block_Appold.txt" )
    os.remove(save_path+"\\remove_Appold.txt")
    os.rename(save_path+"\\remove_Appnew.txt",save_path+"\\remove_Appold.txt" )
    os.remove(save_path+"\\Output.txt")

    
ki=files()
if ki==2:

    with open(os.path.join(save_path, "Block_Appold"+".txt"), "w") as file21:
        for j in si1:
            j=str(j)
            u =j.split("u'")[1]
            
            v =u.split("',)")[0]
            if 'Service' in v:
                 pass
            else:
                file21.write(v+'\n')
    file21.close()
    with open(os.path.join(save_path, "remove_Appold"+".txt"), "w") as file22:
        for k in si2:
            k=str(k)
            e =k.split("u'")[1]
            f =e.split("',)")[0]
            if 'Service' in f:
                 pass
            else:
                file22.write(f+'\n')
    file22.close()
                  
    ki=files()
s=swchanges()

if s ==0:
    print "No file Added "
    alert(0)
else:
    with open(ot, 'r') as o1:
        for i in o1:
            print i
    o1.close()
    alert(1)
    

v=remove()

