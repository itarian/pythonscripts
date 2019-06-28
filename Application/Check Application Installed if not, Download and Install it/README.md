Please specify the full path and name of installation file together with required command parameters. 

Please run the script as System User

Usage Instructions:
ApplicationName='program name to check whether already installed or not'
URL=r'enter your valid URL'
SilentCommand='enter silent commands'
DownloadPath='download path'
FileName='file name you wish to save by' - Please don't keep the extension
Extension='extension with DOT'

Eample,

ApplicationName='7-Zip'
URL=r'https://patchportal.one.comodo.com/portal/packages/spm/7 Zip/x86/7z1604.exe'
SilentCommand='/S'
DownloadPath='%temp%'
FileName='7ZIP1'
Extension='.exe'