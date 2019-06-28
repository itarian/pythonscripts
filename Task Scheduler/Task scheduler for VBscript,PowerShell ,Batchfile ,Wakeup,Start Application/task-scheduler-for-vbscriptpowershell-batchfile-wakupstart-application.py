input=8 #choose your input from Below

#Give the task name to delete if you need

#1)Taskname : standby
#2)Taskname : exestart
#3)Taskname : command
#4)Taskname : Script
#5)Taskname : startapp 
#6)Taskname : batscript
#7)Taskname : VBscript
#8)Taskname : Powershell

task_to_delete=r""   #declare here to delete  scheduled task

#1-------------Wakup(Become active from sleep mode) from standby scheduler **Give DAY and time **Task Name :standby
#2--------------To start Application using task scheduler  **Give the path for Script #2)Taskname : exestart
#3--------------To give Excute Command using task scheduler ** Give Windows command  #3)Taskname : command
#4-------------to run the vbscript from system path using task scheduler **Give Day , Time and Path #4)Taskname : Script
#5------------To start application silently       ** Give path for Script  #5)Taskname : startapp
#6-------------Run custom batch script using task scheduler ****Give Day ,Time And Path for Batch Script    #6)Taskname : batscript
#7------------Run custom VB script **Give Day ,Time and fill Vbscript            #7)Taskname : VBscript
#8-----------Run custom powershell script using task scheduler  **Give Day ,time and Give powershell Script   #8)Taskname : Powershell


#please fill the DAY and Time To schedule

daily="DAILY"   #Eg:DAILY,MON,TUE,WED,THU,FRI,SAT,SUN
time="04:21"    #TIME

execute_path=r'C?C:\Users\Dhoni\Desktop\commands.bat"' #path 

##No need to path for wakup and command

command='ipconfig' #Commands you need to excute
batch_script=r'''

PLEASE GIVE YOUR BATCH SCRIPT HERE YOU NEED TO SCHEDULE

'''
###VBSCRIPT 
vbs_script=r'''
PLEASE GIVE YOUR VBSCRIPT HERE  YOU NEED TO SCHEDULE
'''

##Powershell SCript
powershell_script=r'''


PLEASE GIVE YOUR POWERSHELL SCRIPT HERE YOU NEED TO SCHEDULE
'''
import os
import subprocess
import socket
from ctypes import *
class disable_file_system_redirection:
    _disable = windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value =c_long()
        self.success = self._disable(byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value) 

def startapplication(path):#starts application #Taskname : exestart
    cmd="schtasks /create /tn:exestart /tr:"+path+" /sc:"+daily+" /st:"+time
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print "Task Scheduler Scheduled To Start Application "
    


def restart(daily,time): ######Wakup's the sysytem from standby mode #Taskname : standby
    path=os.environ['TEMP']
    if  os.path.exists(path):
        os.chdir(path)
        print "TRUE"
        with open("Retsrt.bat","w+") as f:
            f.write("hello")
            f.close() 
    cmd="schtasks /create /tn:standby /tr:"+path+" /sc:"+daily+" /st:"+time
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print "Task Scheduler Scheduled To Wakeup the Desktop"

def startapplicationsilently(path):    ##starts the application #Taskname : startapp 
    path2='start '+path
    path4=os.environ['TEMP']
    print path4
    print path
    if  os.path.exists(path4):
        os.chdir(path4)
        print "TRUE"
        with open("Retsrtapp.bat","w+") as f:
            f.write(path2)
            f.close()
    cmd="schtasks /create /tn:startapp /tr:"+path4+"\Retsrtapp.bat /sc:"+daily+" /st:"+time
    print cmd
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print "Task Scheduler Scheduled To Run  Commands of Application  silently "
    
    
def command1(daily,time,command): #excutes the windows command #Taskname : command 
    path=os.environ['TEMP']
    command='"'+command+'"'
    print path
    if  os.path.exists(path):
        os.chdir(path)
        print "TRUE"
        with open("command.bat","w+") as f:
            f.write('start cmd.exe /k '+command)
            f.close()
    
    cmd="schtasks /create /tn:command /tr:"+path+"\command.bat /sc:"+daily+" /st:"+time
    print cmd
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print "Task Scheduler Scheduled To Run the WIndows command "

def script(daily,time,path): #excutes the  VB script #Taskname : Script
    if  os.path.exists(path):
        print "TRUE"
    path='"cscript.exe '+path
    print path
    cmd="schtasks /create /tn:Script /tr:"+path+  " /sc:"+daily+" /st:"+time
    print cmd
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print "Task Scheduler Scheduled To Run the Custom VB Script "
    
def BATFILE(daily,time,wincommands,path): #excutes the windows command #Taskname : batscript
    path=os.environ['TEMP']
    print path
    if  os.path.exists(path):
        os.chdir(path)
        print "TRUE"
        with open("command.bat","w+") as f:
            f.write(wincommands)
            f.close()
    
    cmd="schtasks /create /tn:batscript /tr:"+path+"\command.bat /sc:"+daily+" /st:"+time
    print cmd
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print "Task Scheduler Scheduled To Run the BAT File"

    
def VBSCRIPT(daily,time,wincommands): #excutes the custom vbscript #Taskname : VBscript
    path=os.environ['TEMP']
    print path
    if  os.path.exists(path):
        os.chdir(path)
        print "TRUE"
        with open("cScript.vbs","w+") as f:
            f.write(wincommands)
            f.close()
    
    cmd="schtasks /create /tn:VBscript /tr:"+path+"\cScript.vbs /sc:"+daily+" /st:"+time
    print cmd
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print "Task Scheduler Scheduled To Run Defined VBScript "
    
def POWERSHELLSCRIPT(daily,time,wincommands): #excutes the custom powershell #Taskname : Powershell 
    path=os.environ['TEMP']
    print path
    if  os.path.exists(path):
        os.chdir(path)
        print "TRUE"
        with open("command.bat","w+") as f:
            f.write(wincommands)
            f.close()
    
    cmd="schtasks /create /tn:Powershell /tr:"+path+"\command.bat /sc:"+daily+" /st:"+time
    print cmd
    with disable_file_system_redirection(): 
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out = ping.communicate()[0]
        output = str(out)
        print output
        print "Task Scheduler Scheduled To Run Shell Script "
def delete(task_to_delete):
    print "*******************"
    print "You are deleting scheduled Task of  " +task_to_delete
    command="schtasks /delete /tn:"+task_to_delete+ " /f"
    with disable_file_system_redirection():
        print os.popen(command).read()
    

print  "Computer Name: " +socket.gethostname()
print "IP-Address :"
print  socket.gethostbyname(socket.gethostname())
print "\n"

with disable_file_system_redirection():
    print os.popen('schtasks /Query /FO List | find "TaskName"','r',-1).read()
print "**********************"
if input==1:
    restart(daily,time)
elif input==2:
    startapplication(path)
elif input==3:
    command1(daily,time,command)
elif input==4:
    script(daily,time,path)
elif input==5:
    startapplicationsilently(path)
elif input==6:
     BATFILE(daily,time,batch_script,path)
elif input==7:
     VBSCRIPT(daily,time,vbs_script)
elif input==8:
     POWERSHELLSCRIPT(daily,time,powershell_script)


if len(task_to_delete)>0:
    delete(task_to_delete)