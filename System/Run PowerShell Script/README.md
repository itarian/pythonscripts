Please run the script as System User

The procedure does the following for you,

Gets PowerShell Script Content
Gets File Name with Extension ".ps1"
by the following parameters -

ps_content=r'''

PLEASE PASTE YOUR POWERSHELL SCRIPT HERE

'''

Also Define file_name i.e

file_name='last_boot_time.ps1'

Create the file at Windows Temp Location with the given content
Executes the ps1 file and prints the output to the ITSM Log
Finally, Deletes the ps1 file
By the way, you can change the content and file name if you want to run another PowerShell script.

 

ps_content=r'''function Get-Uptime { Param( $ComputerName = $env:COMPUTERNAME ) if ($lastBootUpTime = (Get-WmiObject win32_operatingsystem -ComputerName $ComputerName| select @{LABEL='LastBootUpTime';EXPRESSION={$_.ConverttoDateTime($_.lastbootuptime)}}).LastBootUpTime) { (Get-Date) - $lastBootUpTime } else { Write-Error "Unable to retrieve WMI Object win32_operatingsystem from $ComputerName" } } Get-Uptime''' file_name='last_boot_time.ps1'