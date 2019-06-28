Hi

Please refer the wiki below guide before you proceed to the script to install acronics client backup app

https://wiki.comodo.com/frontend/web/topic/how-to-prepare-offline-installer-and-deploy-acronis-agent-remotely-using-script-procedure

Description: wiki guide helps you to create offline installer for acronis backup agent and by providing the offline installer download  link  in the script

It allows you automatically register/enroll your device with your appropriate company associated with account https://us-cloudbackup.comodo.com/

Note: Run this script as system user only

Edit parameters:

if os.path.exists("C:\Program Files (x86)"):
    URL=r"https://onedrive.live.com/download?cid=A910C8EF113350FB&resid=A910C8EF113350FB%21112&authkey=AMECL8aODL9m3ls" ####provide an URL of 64 bit package
else:
    URL=r"https://onedrive.live.com/download?cid=A910C8EF113350FB&resid=A910C8EF113350FB%21113&authkey=AFjGrLU57CvNhkY" ####provide an URL of 32 bit package