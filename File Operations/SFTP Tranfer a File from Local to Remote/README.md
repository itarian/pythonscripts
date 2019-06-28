This script to upload the list of files in SFTP method using any third party application .

Input Parameters:
1.Filelist - Enter the filename that needs to be transferred from your local machine to server.
Example : "C:\\Users\\Administrator\\Desktop
regex.txt"
2.PrintLog - Helps to modify the output of the procedure by either printing the log and not printing the log
0 - Enter 0, to not print the log file data
1 - Enter 1, to print the log file data

Example :

PrintLog=0

3. Server - Login into the server with username and password 

  Example:

       Server="sftp://Username:password@example.server.com/" 

4. des - Path of server where the file to transfer

Example: 

       des= "/folder name/file"

Please run this script as logged in User

 

This Script run as Logged in user