This script is used to change time zone and run the specified .bat and .exe file from network location.

Provide the following parameters:

name='"Syria Standard Time"'   #provide the name of the time zone to be changed
#If name is in string, enclose it in '" "'- eg:'"Syria Standard Time"'
#If name is in String+number, enclose it in " " - eg: "UTC+13"

Filepath=r'\\Audi\c\Users\audiR7\Desktop'            ##Provide the network share file path
share_user="XXXXX"                                             ## Provide the user name for the shared path
share_pass="YYYYY"                                            ## Provide the password for the shared path
Setup_Path_X64=r"qbittorrent_4.1.0_x64_setup.exe"         ## Enter the .exe file name for 64 bit
Setup_Path_X86=r"qbittorrent_4.0.4_setup.exe"                 ## Enter the .exe file name for 32 bit
Bat_file=r"Sample.bat"                  ## Enter the .bat file name
silent_commnad ="/S"                   ## Enter the silent command to install the .exe file