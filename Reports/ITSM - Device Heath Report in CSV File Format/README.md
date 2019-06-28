Please use the script to get Procedure Finished Success, Procedure Finished Fail, Procedure parsed Successfully, Installed Critical and Security Patches, Installed patches with installed date and Hard Disk Properties.

Note:
Please modify the variables as per your concern

sendmail=0 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out an email from the code.
msgbody=r'''Hi

Please find the attachment for the Computer Health Report in CSV file format.

Thank you.'''
 

emailto=['abc@yopmail.com']      # Provide an email where want to send CSV file.
emailfrom='xyz@gmail.com'        # Provide a valide from email.
password='******'                           # Provide the correct password for your from mail.
smtpserver='smtp.gmail.com'
port=587

 

CSV Separator: 
Use '|' as a separator when you open the csv [output file]

 

To Enable Email:

Change the variable as follows

sendmail=1

Please Run as system user.