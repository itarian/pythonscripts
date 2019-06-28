This script is used to download and install teamviewer host.

Run the script as " SYSTEM USER ".

Note :

1.Provide the download URL at the first line of the script .

Download_URL ="https://dl.tvcdn.de/download/TeamViewer_Host_Setup.exe"   #Provide the download URL here

2.Provide the .reg file in the content(second line of the script) within the quotations '''' xxxxxxx''''.  

content ='''Windows Registry Editor Version 5.00                         

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TeamViewer]
"Start"=dword:0x000000002
'''