This script will collect all the Windows Logs on the endpoint and send those logs report as the zip file to the mail. That zip file has all types of logs like Critical , Severe , Error , Information.

NOTE:

zip_fname  = r'Windows_Logs.zip'            #Give the name for your Output Zip file

emailto      = ['abc@yopmail.com']           # Provide an email where want to send Output zip file.

emailfrom   = 'xyz@gmail.com'                # Provide a valide from email.

password   = '*********'                             # Provide the correct password for your from mail.

sendmai     = 1                                       ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email.

Run as SYSTEM USER.