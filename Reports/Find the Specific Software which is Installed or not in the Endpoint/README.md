Hi

This Script will help you to find the specific software which is installed or not on the selected Devices or All the devices as one report and sends an Email.

Define the following variables for better output:

find=['xx','yy']               #Given the specific software name you need to find on your devices  Eg.['comodo client - communication','Google Chrome','Mozilla Thunderbird']
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
****************************************************************************************************************************************************

NOTE:

Please Run this Script as System User