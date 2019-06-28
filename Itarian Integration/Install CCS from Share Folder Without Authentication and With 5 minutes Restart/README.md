This script will install CCS from the Network share without authentication and with the 5min restart. Please ensure that you have setup file in the network share.

NOTE:

    #Do you want to show Installation notes  
    showwarn="yes"                                                            ## provide yes or no. If showwarn="yes" , Installation Message will appear
     Do you want to enable MSI Installation log
    msiLogs = "yes"                                                            ## provide yes or no. If msiLogs="yes" , Installation log will appear
    Source_Path=   r'\\Win-biktodgscbo\f'                                        ##Provide the network share file path
    File_Name_64=  r'CIS_x64.msi'         ## Enter the .msi file name for 64 bit
    File_Name_86 = r'CIS_x86.msi'         ##  Enter the .msi file name for 32 bit

 

This script will install CCS from the Network share without authentication and with 5min restart. Please ensure that you have setup file in the network share.

Note: Must be provided Source_Path = r'\\ad\Shared' that is Shareable to path user.
