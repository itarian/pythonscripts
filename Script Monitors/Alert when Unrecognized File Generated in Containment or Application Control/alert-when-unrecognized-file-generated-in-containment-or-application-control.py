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


doll1=''
doll2=''

flag=0
global fnd2
fnd2=0

ot=save_path+"\\Output.txt"

conn = sqlite3.connect('C:\ProgramData\Comodo\Firewall Pro\cislogs.sdb')
cur1 = conn.cursor()

cur1.execute("SELECT Path FROM SbEvents where Rating=1")

rows1 = cur1.fetchall()

for j in rows1:
    si1.append(j)

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 
def files():
    file_name1 = "Unrecognized_Appold.txt"
    cur_dir1 = save_path
    file_list1 = os.listdir(cur_dir1)
    parent_dir1 = os.path.dirname(cur_dir1)
    if file_name1 in file_list1:
        fnd2=1
        with open(os.path.join(save_path, "Unrecognized_Appnew"+".txt"), "w") as file21:
            for j in si1:
                j=str(j)
                file21.write(j+'\n')
                fnd2=1      
    else:
        with open(os.path.join(save_path, "Unrecognized_Appold"+".txt"), "w") as file21:
            file21.write('\n')
            fnd2=2  
    return fnd2
def swchanges():  
    file11=save_path+"\\Unrecognized_Appnew.txt"
    file21=save_path+"\\Unrecognized_Appold.txt"
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
                   o1.write("\n**********  Unrecognized Files***********\n")
                   for line in diffList1:
                       if line[0] == '-':
                           flag=1
                           o1.write("File has Added  :"+ ''.join(re.findall('u(.*),',line))+'\n')
               o1.close()  
           file.close()
        file.close()
    return flag 
def remove():
    os.remove(save_path+"\\Unrecognized_Appold.txt")
    os.rename(save_path+"\\Unrecognized_Appnew.txt",save_path+"\\Unrecognized_Appold.txt" )
    os.remove(save_path+"\\Output.txt")
ki=files()
if ki==2:
    with open(os.path.join(save_path, "Unrecognized_Appold"+".txt"), "w") as file21:
        file21.write('\n')
    file21.close()
    ki=files()
s=swchanges()


if s ==0:
    print "No file has Added "
    alert(0)
else:
    with open(ot, 'r') as o1:
        for i in o1:
            print i
    o1.close()
    alert(1)
v=remove()
