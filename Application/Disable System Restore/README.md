Hi,

This script is used to disable the system restore point on your endpoint.

Refer the wiki to run the procedure with parameters
https://wiki.comodo.com/frontend/web/topic/how-to-create-and-run-procedures-with-parameters

For Example:

drive="c:" #Provide the drive which you need to disable Restore Access

The above parameters should be obtained from the customer for disabling system restore. 

Note: Please edit the following parameters in the script

### PARAMETERS TO BE EDITED UNDER PARAMETERS TAB ###

1.Provide_drive_for_system_restore:
   TYPE: String
    EM LABEL: Any name
   Default value: "Provide the drive which you need to disable system restore"

 

Run as System User
