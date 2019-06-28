This Script will generate alert if any file is Encrypted in Specified path and Trigger the VEEAM AGENT BACKUP to backup the given path.

Output will have User details of where and when file is encrypted (i.e) created, modified date and time of encrypted file, owner of Encrypted file and Veeam agent status in the Endpoint.

NOTE:

    Please ensure that " VEEAM AGENT BACKUP " is installed in endpoint.
    Path = r"C:\ProgramData"                                             #Give the path want to Monitor.
    path_to_bckup=r"C:\Users\C1-En_230\Desktop\Backup" #Give the path where want to store backedup files.

 
Run as System User
