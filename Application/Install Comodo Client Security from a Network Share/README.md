This script will install CCS from a Network share. Please ensure that you have the specified setup file in the network share.

Steps to follow:

1.you have to pass the filepath, share_user, share_pass, Setup_Path_X64, Setup_Path_X86 in the parameter section.
Refer the wiki to run the procedure with parameters
https://wiki.comodo.com/frontend/web/topic/how-to-create-and-run-procedures-with-parameters

NOTE:
1.Enter_the_share_path:
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter your network share path location"

2..Enter_the_share_user :
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter the shared user name"

3.Enter_the_share_pass :
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter the password of the shared user"

4.Enter_the_share_setup_64:
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter the file name of the file in network share for 64 bit along with extension"

5.Enter_the_share_setup_32:
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter the file name of the file in network share for 32 bit along with extension"

For Example:

    Filepath=   r'\\Win-biktodgscbo\f'                                        ##Provide the network share file path
    share_user=  "abc"                                                 ## Provide the user name for the shared path
    share_pass=  "xyxz"                                               ## Provide the password for the shared path
    Setup_Path_X64=  r"CIS_x64.msi"     ## Enter the .msi file name for 64 bit
    Setup_Path_X86=  r"CIS_x86.msi"     ##  Enter the .msi file name for 32 bit

 

Run as SYSTEM USER
