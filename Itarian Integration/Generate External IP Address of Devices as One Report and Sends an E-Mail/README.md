Hi

The Script will help you to get all External IP Address of Selected Devices or All devices as one report and sends an Email

Define following variables for better output

no="xx"        #Edit the xx parameter as Device Timeout. Eg if you have 500 enrolled endpoints then that xx must "100".
Head_computer=r'LAVA-PC' # Head computer to send the email
key=r'CHANGE ME'   # define your own unique key identification
emailto='kupido@yopmail.com' # Email address to send the report

*****************************************************************************************************************************************************

CAUTION :

Defining Head Computer is Mandatory i.e(Head_computer=r"LAVA-PC" )

Head Computer send an Email collecting from all devices

Defining Key is mandatory otherwise there are chances of data getting collided with other users data

From the key we have to idenitfy the preffered  MSP or USER. i.e it acts as unique identification key

Defining no is Mandatory

no="xx" xx value acts Device timeout value that is how much time that the headcomputer will wait for their clients to receieve reports.it is time range based on the number of end points

Eg if you have 500 enrolled endpoints then that xx must "100".
*****************************************************************************************************************************************************

 

Hi The Script will help you to get all External IP address of Selected Devices or All devices as one report and sends an Email Define following variables for better output no="xx" #Edit the xx parameter as Device Timeout. Eg if you have 500 enrolled endpoints then that xx must "100". Head_computer=r'LAVA-PC' # Head computer to send the email key=r'comodo' # define your own unique key identification emailto='kupido@yopmail.com' # Email address to send the report ***************************************************************************************************************************************************** CAUTION : Defining Head Computer is Mandatory i.e(Head_computer=r"LAVA-PC" ) Head Computer send an Email collecting from all devices Defining Key is mandatory From the key we have to idenitfy the preffered MSP or USER. i.e it acts as unique identification key Defining no is Mandatory no="xx" xx value acts Device timeout value that is how much time that the headcomputer will wait for their clients to receieve reports.it is time range based on the number of end points Eg if you have 500 enrolled endpoints then that xx must "100". *****************************************************************************************************************************************************

NOTE:

Please Run this Script as System User
