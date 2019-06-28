This script  to backup  an file,folder and Drive from your computer to Acronis cloud backup. Acronis Backup and Acronis Backup Advanced are a disk-based backup and recovery programs

NOTE:

*** This Script Can Backup the System Drive But Recovering the System Drive from Acronis using this script is Strictly not Recommended (It Causes System Crash) ***

1.Before running this script its mandatory you run the Acronis Service Configuration script from the following link

https://scripts.comodo.com/frontend/web/topic/acronis-service-configuration.

2.In username and password field please provide the Acronis account username and password.

3.Assign input=1 in program if you want to backup the folder

4.Assign input=2 in program if you want to backup the file

5.Assign input=3 if you want to backup the drive

6.If your input is 1 or 2 in program provide the path for the file or folder to be backed up

7.You can refer the below table for the list of parameters that needs to given according to your Task

TASK
	

EDITABLE PARAMETERS

1.Backing up folder
	

BackupPathfolder

2.Backing up the file
	

BackupPathfile

3.Backing up the DRIVE
	

Backupdisk

4.Recovering up the folder
	

ArchieveName,acronispath,RecoverydestinationPath

5.Recovering up the File
	

ArchieveName,acronispath,RecoverydestinationPath

6.Recovering up the drive
	

AcronisRecoverdrive,AcronisTargetDrive

Please run this script as an logged in User
