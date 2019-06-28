Hi,
Please refer the below script for log collection of last 48 hours browsing history and user actions.
This script will display the browsing history of all web browsers which are present in your system and get the information of all what the user can browse over last 48 hours and the ,1) Microsoft UAC "requests" for privilege action toward user 2) Usage of user account with admin rights (in the case of user authenticate with admin account, or use admin account in a UAC request, 3)To receive an alert when a user accept UAC (or) input admin account in UAC and to know for which process it was requested and track in audit report this kind of actions to investigate in case of security issue.
These all information are sent through mail to particular email id which you are mentioned and tit will display in the CSV format
For more information please refer the below screenshots to download the attachment and read the CSV file.
Please run the script as the system administrator.

Note:
Please modify the variables as per your concern
sendmail=1 ## [1- sends csv reports in email or 0- prints output in execution logs ] if sendmail=1 then user have to set the required information to send out a email from the code .
msgbody='Hi,\n\nPlease find the attachment for the Computer Health Report in CSV file format.\n\nThank you.'
emailto=['xxxx@gmail.com']
emailfrom='yyyy@gmail.com'
password='zzzzzzzzzz'
smtpserver='smtp.gmail.com'
port=587

