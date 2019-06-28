Hi,

This script checks whether Microsoft office 2016 has been installed in your endpoint.If not it will download and install the package on your endpoint. You can also modify the parameters for XML depending upon your environment.

Edit Parameters:

OfficeClientEdition="32" #Installs the edition of office
Channel="Targeted" #Installs the Office installation files from Semi-Annual Channel 
Product_ID="O365ProPlusRetail" #Installs Office 365 ProPlus
Language_ID="en-us" #Installs English version of Office 

Display_Level="None" #Displays the installation progress

 

Run as System User.
