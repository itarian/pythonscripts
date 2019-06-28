path=r"C:\Users\lanadelrey\Downloads\New folder" #Provide path for monitoring changes 
Review_Folder=r"C:\Users\lanadelrey\Desktop"     #Provide path where output file is to be generated for review
import os
import re
import filecmp
import difflib
import sys

workdir=os.environ['PROGRAMDATA']+r'\c1_temp'
if not os.path.exists(workdir):
    os.makedirs(workdir)

save_path=workdir

Review_Folder=os.path.join(Review_Folder,"File_review.txt")
if os.path.exists(Review_Folder):
    try:
        os.remove(Review_Folder)
    except:
        pass
flag=0
global fnd
fnd=0
global fnd1
fnd1=0


def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

def swchanges():
    listfiles=[]
    file1=os.path.join(save_path,"read_new.txt")
    file2=os.path.join(save_path,"read_old.txt")
    flag=0
    if False==0:
        
        with open(file1) as file:
           data=file.read()
           with open(file2) as file:
               data2=file.read()
               text1Lines = data.splitlines(1)
               text2Lines = data2.splitlines(1)
               diffInstance = difflib.Differ()
               diffList = list(diffInstance.compare(text1Lines,text2Lines ))
               for line in diffList:
                 if line[0] == '-':
                     flag=1
                     listfiles.append("File has Added :"+path+"\\"+line+"\n")
                     print "File has added: "+path+"\\"+line
               diffList = list(diffInstance.compare(text2Lines, text1Lines))
               for line in diffList:
                 if line[0] == '-':
                    flag=1
                    print "File has removed: "+path+"\\"+line
                    listfiles.append("File has Removed :"+path+"\\"+line+"\n")
        if flag==1:
            with open(Review_Folder,"w") as f:
                for i in listfiles:
                    f.write(i)
        return flag
def files():
    file1=os.path.join(save_path,"read_new.txt")
    file2=os.path.join(save_path,"read_old.txt")
    os.chdir(path)
    output=os.popen("dir /a /b /o:n").read()
    if os.path.exists(file2):
        with open(os.path.join(file1), "w") as f:
            f.write(output)
        change=swchanges()
        with open(os.path.join(file2), "w") as f:
            f.write(output)
        os.remove(file1)
    else:
        change=0
        with open(os.path.join(file2), "w") as f:
            f.write(output)
    if change==0:
        return 0
    else:
        return 1
                  
        
        

s=files()

if s ==0:
    print "No file has Added or Removed"
    alert(0)
else:
    os.popen("msg * /time:600 Please check this file %s to review your files"%(Review_Folder))
    alert(1)


    
    
        

