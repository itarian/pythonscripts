Please refer below script to email Event Logs 

Edit parameters:
sendemail=0->Edit "sendemail=0" to send report in email or Edit "sendemail=1" to print the output in ITSM portal

Edit Email recipients and smtp details if sendemail=1 is set
emailto =['xyz@gmail.com','pqr@gmail.com'] 
emailfrom = "yyyyyy@gmail.com"
password = "12345678"
smtpserver='smtp.gmail.com'
port=587