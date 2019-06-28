This script is used to collect comodo one logs using cisreporttool.
Running this script will download the cisreporttool and run this tool which will collect all comodo one logs as a  compressed single zip file.

The collected zip file will be sent automatically to the sftp server in the  below mentioned filename format.

For Example:
CisReportData_DESKTOP-NI6H3HS_2018-04-18_15-44-47.zip

In the Above mentioned Example filename "CisReportData" is default name followed by the computer name with the TImestamp (Date(yyyy-mm-dd),time(hh:mm:ss))
 

Please run the script as system user 