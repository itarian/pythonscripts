Hi ,

The script gets System Information and software's which are installed on endpoint

Note :

The script can run on both System user and Logged in user

These all information are sent through mail to particular email id which you are mentioned and tit will display in the CSV format
For more information please refer the below screenshots to download the attachment and read the CSV file.

Please modify the variables as per your requirement 
sendmail=1 ## [1- sends csv reports in email or 0- prints output in execution logs ] if sendmail=1 then user have to set the required information to send out a
email from the code .
msgbody='Hi,\n\nPlease find the attachment for the System Information and Installed Softwares List.\n\nThank you.'
emailto=['xxxxxxxxxxxxx@comodo.com']
emailfrom='testcomodomail1@gmail.com'
password='C0m0d0@123'
smtpserver='smtp.gmail.com'
port=587