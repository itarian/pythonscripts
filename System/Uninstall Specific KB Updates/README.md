Hi,
Please refer to the script for uninstalling the specific KB_updates from your system.
This script will display the list of KB Update packages present in your system, If you provide any specific update number in the below script then, it will uninstall it. or Otherwise, If you don't provide any kb_update package in the below script then it will display the list of packages present in it and Finally, it will ask you to provide any specific kb_update package to uninstall.

NOTE: Update for the specified KB is required and so certain KB cannot be uninstalled. Kindly refer the following file "C:\Windows\Logs\DISM" to view the error logs.


Instructions:

1.First time when you run the script:: It will display the list of kb_updates present in your system and then It will give the message like 'Please provide kb_update number in the kb_list_user list', If there is No kb_update package present in your system then it will display like this 'No KB_UPDATES for security/update found in your system '
2. From the output you will get to know the kb_update number from the list of packages, just have to give the KB number
For Example:

PARAMETERS TO BE EDITED:

KB_to_Uninstall:

Type: List
Label: Any name
Possible Items: Kb values
Default Value: Select KB values from the possible items

Note: Update for the specified KB is required and so certain KB cannot be uninstalled. 

Kindly refer the following file "C:\Windows\Logs\DISM" to view the error logs.