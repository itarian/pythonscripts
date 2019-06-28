Hi,

The script helps you to Collect the Windows Update logs of the System and transfer the files to SFTP server.

Edit Parameters:

    Define  kayako_ticket_number="XXXXXXXXXX"  

it will uploaded windows update.log file as compressed zip file and that will be sent automatically to the sftp server in the  below mentioned filename format.

For Example:
GOI-221-286602_WINDOWSUPDATELogData_DESKTOP-MKQ58SO_2018_04_26_20_02_58.zip

 

In the Above mentioned Example filename "kayako_ticket_number"  is followed by the "WINDOWSUPDATELogData" with the computer name and the TImestamp (Date(yyyy-mm-dd),time(hh:mm:ss))
 

Please run the script as system user 