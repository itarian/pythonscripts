import os
import difflib, sys

programdata = os.environ['PROGRAMDATA']
folder      = os.path.join(programdata,"C1_Temp")
list_tasks = os.popen("schtasks.exe /Query /FO List").read()

def createlist(folder,list_tasks):
    os.chdir(folder)
    if os.path.isfile("SchdeuledTaskListadd.txt"):
        print ""
    else:
        with open("SchdeuledTaskListadd.txt","w+") as f:
            for i in [i.strip() for i in list_tasks.split('\n') if 'TaskName'  in i if i.strip()]:
                list02 = i[15:]
                f.write(list02+"\n")

    with open("SchdeuledTaskListadd_latest.txt","w+") as f:
        for i in [i.strip() for i in list_tasks.split('\n') if 'TaskName'  in i if i.strip()]:
            list01 = i[15:]
            f.write(list01+"\n")
    
def filecmpadd():
    with open("SchdeuledTaskListadd.txt") as f1:
        s2 = set(f1)
    with open("SchdeuledTaskListadd_latest.txt") as f2, open("SchdeuledTaskList03.txt","w+") as f3:
        f3.writelines(x for x in f2 if x not in s2)  
    if os.path.isfile("SchdeuledTaskList03.txt") and os.path.getsize("SchdeuledTaskList03.txt") > 0:
        with open("SchdeuledTaskList03.txt","r+") as f3:
            diff_list = f3.read()
            with open("SchdeuledTaskListadd.txt","a") as f:
                f.write(diff_list+"\n")
            print  "New schduled task  has been added\n"
            print "TaskName is"
            print diff_list
            alert(1)
    else:
        alert(0)
        print "No new schduled tasks been added"
    os.remove("SchdeuledTaskList03.txt")
    os.remove("SchdeuledTaskListadd_latest.txt")
    

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 
            


if os.path.exists(folder):
    if createlist(folder,list_tasks):
        print createlist(folder,list_tasks)
    else:
        print createlist(folder,list_tasks)  
        print filecmpadd()
    
else:
    os.chdir(folder)
    os.mkdirs("C1_Temp")
    if createlist(folder,list_tasks):
        print createlist(folder,list_tasks)
    else:
        print createlist(folder,list_tasks)   
        print filecmpadd()
    
