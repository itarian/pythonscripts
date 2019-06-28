This script is used to set value in registry

Input:

Key=Here give the path of registry to change

Sub_Key=Mention the sub_key of registry

Field=Mention the field name 

Value=Give the value of the registry

Example:

Key= "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
Sub_Key= "NoAutoRebootWithLoggedOnUsers"
Field= "REG_DWORD"
value = "1"

This Script run as a "System User"

 

This Script run as a system user