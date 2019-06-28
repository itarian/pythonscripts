Hi

The Script will help you to get all the windows operating system version details  of selected devices as text report and sends an Email

Eg.


OS Name:                   Microsoft Windows 10 Enterprise

OS Version:                10.0.17134 N/A Build 17134

OS Manufacturer:           Microsoft Corporation

OS Configuration:          Standalone Workstation

OS Build Type:             Multiprocessor Free

BIOS Version:              innotek GmbH VirtualBox, 12/1/2006

 

 

Define following variables for better output

emailto=['pandi@yopmail.com']  # Provide an Toemail address where the report need to be sent.You can also provide any number of To email address For example: ['pandi@yopmail.com','sensor@yopmail.com']
emailfrom='coneoperations@gmail.com' # Provide from email address
password='*********' # Provide Password
smtpserver='smtp.gmail.com'
port=587

 

 

Note:

Run the Script as System User

Edit the mandatory parameters before running the script.