This script procedure run PowerShell command and prints the output to the ITSM Log. We can run the script procedure as either "system user" or "logged in user".

ps_command=r'Get-Childitem C:\\Windows\\*.log'