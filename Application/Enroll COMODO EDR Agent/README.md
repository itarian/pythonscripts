Hi,

This script helps you to automate the enrollment of the Comodo Endpoint Detection and Response agent.

Steps to follow:

    Log in to your https://edr.cwatch.comodo.com and download EDR agent that is specific to particular customers.
    Upload the file in your hosted environment to get a direct download link. For example, Onedrive         
    Edit the "URL" and "FileName" options in the script procedure
    Run the script procedure in the required endpoints

For example:

URL = r'https://onedrive.live.com/download?cid=A910C8EF113350FB&resid=A910C8EF113350FB%21116&authkey=AOfmMyN4yDuVkXU'

FileName = 'Comodo_EDR_Agent_Installer_1.1.258.3_ByN3AlxAz'

Extension = '.exe'
          

NOTE:

In FILENAME there will be a 9 digit word  ("ByN3AlxAz'") which is unique for every User, and ensure that the FileName you have entered is correct as it was downloaded from https://edr.cwatch.comodo.com

###  PARAMETERS TO BE EDITED UNDER PARAMETERS TAB  ###

1.Enter_the_URL:
 TYPE: String
 ITSM LABEL: Any name
 Default value: "Enter your URL"

2.Enter_the_filename:
 TYPE: String
 ITSM LABEL: Any name
 Default value: "Enter your filename"

3.Enter the Extension:
 TYPE: String
 ITSM LABEL: Any name
 Default value: "Enter the Extension". For Eg: .exe
 

Run the script as "System User"

TESTED PLATFORM:

 Windows: 10, 8.1, 8, 7.
