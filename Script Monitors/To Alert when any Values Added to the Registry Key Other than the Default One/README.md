Hi,

please refer this script to  alert when any values added to the registry key other than the default one.

If the alert is in ON state, you can find the updated registry details in the file at the following path: "C:\Progrm Data\registry.txt" inside the device.

Edit parameters:

reg_path=['xxxxxxxxxxxxxxxxxxx','yyyyyyyyyyyyyyyyyyyyyyy']  #edit with your registry path here

You can even provide more than one registry key separated by commas as shown below:

For example:

reg_path=['HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Connection Manager','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\DirectDraw']

 

Note: Run as custom monitoring script Instructions as below https://wiki.comodo.com/frontend/web/topic/how-to-use-custom-script-procedure-monitoring