Hi,

This script will help you to automatically unenroll from one EM portal and enroll in another EM portal. 
Refer the wiki to run the procedure with parameters
https://wiki.comodo.com/frontend/web/topic/how-to-create-and-run-procedures-with-parameters

For Example:

host="comodopmsupport-comodopmsupport-msp.cmdm.comodo.com"  
port="443"                                                                                                 
token="7d091a7436635bac6743a02d1e158fa8"   

The above parameters should be obtained from the new EM portal in which the device needs to enrol.

Note: Please edit the following parameters in the script

### PARAMETERS TO BE EDITED UNDER PARAMETERS TAB ###

1.Enter_the_Host_name:
   TYPE: String
    EM LABEL: Any name
   Default value: "Enter your hostname of new EM portal which you want to enroll"

2.Enter_the__port_name:
   TYPE: integer
    EM LABEL: Any name
    Default value: "Enter your port number of the EM Portal"

3.Enter_the_Token:
   TYPE: String
   EM LABEL: Any name
  Default value: "Enter the Token of the EM Portal"

Please run the script as "System user"      