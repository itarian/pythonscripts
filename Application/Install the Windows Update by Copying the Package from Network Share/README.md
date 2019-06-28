This script will install the windows update by copying the package from network share.

The script will check if the the update is already installed or not.If the update is not installed it will copy the .msu file from the network share and silently install the windows update successfully.

Note : Provide the following parameters

Filepath=r'\\TEDDYBEAR-PC\Desktop'                                        ##Provide the network share file path for example: \\TEDDYBEAR-PC\Desktop
share_user="xxxxxxxxx"                                             ## Provide the user name for the shared path
share_pass="yyyyyyyyy"                                               ## Provide the password for the shared path
Setup_Path_X64=r"windows10.0-kb4103714-x64.msu"     ## Enter the .msu file name with extension for 64 bit for example : windows10.0-kb4103714-x64.msu
Setup_Path_X86=r"windows10.0-kb4103714-x86.msu"     ##  Enter the .msu file name with extension for 32 bit for example : windows10.0-kb4103714-x86.msu
kbvalue=r"KB4103714"                                ## Enter the KB value of the update for example: KB4103714
 