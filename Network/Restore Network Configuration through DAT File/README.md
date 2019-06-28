The script restores the Network Configuration File through the command "netsh" from the given file. Please give the valid file and ensure the file has .dat extension as well.

Note:

Run the following command for generating the Network Configuration .dat file and transverse to the specified path. 

i.e, C:\Users\Administrator\Desktop

netsh interface dump > MyNetworkCFG.dat

Then provide the entire file path in dat_file_path for restoring the network configuration.

You can run the procedure as System User

 

 

 

 

dat_file_path=r"C:\Users\Administrator\Desktop\MyNetworkCFG.dat" - you can change the parameter value to change the path of the DAT file.