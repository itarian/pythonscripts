Filelist =[r"C:\Users\xxx\Desktop\output.txt","C:\User\yyy\Desktop\Out.txt"]## Here you can specifies your list of file path 
PrintLog = 0 ## Printlog can be given either as 0 or 1.
Server = "sftp://Username:password@example.server.com/" ## here specifies your server Link
des="/folder/destination" ## path of folder to transfer file
import os
import zipfile
import urllib
import ssl
import urllib
import time
     
def DownloadSCP():
    temp_path=os.environ['TEMP']
    temp_file=temp_path+r'\winscp.exe'
    f=urllib.urlopen("https://dl.cmdm.comodo.com/download/aa843588-e4ce-4fd3-aa00-864f3352839e/WinSCP_C1_SFTP.exe")
    data=f.read()
    with open(temp_file, "wb") as code:
        code.write(data)
    return temp_path
    
    

def SftpTransfer(FileToSend, Server, des, Path):
    #Script file
    instruction="""
open %s -hostkey=*
cd %s
put "%s"
close
exit
"""%(Server,des,FileToSend)
    #Write the file
    os.chdir(Path)
    with open('run.txt',"w+") as obj:
        obj.write(instruction)
    obj.close()
 #Execute the command
    os.chdir(Path)
##    print Path
    try:
        out=os.popen('winscp.exe /script=run.txt /log=transferlog.log').read()
        with open(Path+r'\transferlog.log',"rb+") as f:
            out=f.read()
        f.close()
        time.sleep(10)
        transferlog=open(os.environ['TEMP']+"\\transferlog.log","a")
        transferlog.write(out)
        transferlog.close()
        print ("The File "+FileToSend+" SFTP upload completed successfully!")
    except ValueError:
        print("No File uploaded")
            

def main():
    Path =  DownloadSCP()
##    print Path
    for FileToSend in Filelist:
        if os.path.isfile(FileToSend):
            SftpTransfer(FileToSend, Server, des, Path)
        else:
            print("The File or path "+FileToSend+" does not exists")
    if PrintLog == 1:
        Readlog=open(os.environ['TEMP']+"\\transferlog.log","r")
        Displaylog=Readlog.read()
        print Displaylog
        Readlog.close()
        time.sleep(5)
    else:
        if PrintLog == 0:
            if os.path.isfile(FileToSend):
                RemoveFile=os.remove(os.environ['TEMP']+"\\transferlog.log")
                
if __name__=="__main__":
    main()
