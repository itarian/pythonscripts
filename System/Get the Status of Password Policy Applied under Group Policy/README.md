This script will retrieve Applied Password Policy status from endpoint under Group policy as a report and sends the report to the preferred mail address.

Run this Script as " SYSTEM USER "

This script will very that the system has applied policies with following configurations. If not it will throw an alert and show actual configurations :

MinimumPasswordAge   = 0
MaximumPasswordAge  = 90 
MinimumPasswordLength  = 7
PasswordComplexity  = 1
PasswordHistorySize   =  4
Give the receiver email address:
Eg:- emailto= "xxx@yyy.com"   #To define a particular receiver email address here