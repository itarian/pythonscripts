Hi

The Script will help you to get all  Virus Database Status (Comodo Client Security) of Selected Devices or All devices as one report and sends an Email

Define following variables for better output

no="xx"        #Edit the xx parameter as Device Timeout. Eg if you have 500 enrolled endpoints then that xx must "100". 
Head_computer=r'LAVA-PC' # Head computer to send the email
emailto='kupido@yopmail.com' # Email address to send the report

*****************************************************************************************************************************************************

CAUTION :

Defining Head Computer is Mandatory i.e(Head_computer=r"LAVA-PC" )

Head Computer send an Email collecting from all devices

Defining no is Mandatory

no="xx" xx value acts Device timeout value that is how much time that the headcomputer will wait for their clients to receieve reports.it is time range based on the number of end points

Eg if you have 500 enrolled endpoints then that xx must "100".
*****************************************************************************************************************************************************

Please Run the Script as System User and also edit the mandatory parameters before running the script.
