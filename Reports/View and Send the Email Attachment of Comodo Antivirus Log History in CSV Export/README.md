Please refer below script to email Threat. Quarantine and Containment history in CSV format. 

Edit parameters:
sendemail=1 ->Edit "sendemail=1" to send csv report in email or Edit "sendemail=0" to print the output in ITSM portal

Edit Email recipients and smtp details if sendemail=1 is set
emailto =['xyz@gmail.com','pqr@gmail.com'] 
emailfrom = "yyyyyy@gmail.com"
password = "12345678"
smtpserver='smtp.gmail.com'
port=587

 

CSV Separator: 

Set CSV separation format as comma ',' for readability