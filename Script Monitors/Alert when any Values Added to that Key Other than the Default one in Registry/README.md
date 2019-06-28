Hi,

please refer this script to alert when any values added to that key other than the default one in the registry.

If the alert is in ON state, you can find the updated registry details in the file at the following path: "C:\Progrm Data\registry.txt" inside the device.

Edit parameters:

reg_path=r"**************" (edit with you registry path)

for ex:reg_path=r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Connection Manager"

 

Note: run as custom monitoring script Instructions as below https://wiki.comodo.com/frontend/web/topic/how-to-use-custom-script-procedure-monitoring