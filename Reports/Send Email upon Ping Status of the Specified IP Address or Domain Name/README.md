Please run the script as System User

This script can be used to send email based on ping status of the domain name or IP given by the user.

NOTE:

The following would be changed for receiving the mail to concern person.

pingip=r"CHANGE_ME"   #Provide the domain name or IP address to ping
Send_Email=1                #Provide 1 if you want to send ping status report as an mail or Provide 0 if you don't want to send an mail.
emailto=r"CHANGE_ME" #Provide the email id for which the report will be sent if you have provided Send_Email as 1