The Script will send the patch reports to your email. You must run the script as a system user.

Note:
Please modify the variables as per your concern

sendmail=0 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out an email from the code.
msgbody=r'''Hi

Please find the attachment for the Endpoints SPMLogs in Text file format.

Thank you.'''
 

emailto=['abc@yopmail.com']      # Provide an email where want to send report file.
emailfrom='xyz@gmail.com'        # Provide a valid from email.
password='******'                           # Provide the correct password for your from mail.
smtpserver='smtp.gmail.com'       #Provide the correct smpt server
port=587                                       #Provide the correct port number

Thank you.

Run the script as a system user.