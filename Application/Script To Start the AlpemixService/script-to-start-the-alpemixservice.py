NP=r"\\DESKTOP-F1HQ8TR\Users\Administrator\Downloads\AlpemixService.exe"  #Mention the network share path which contains AlpemixService.exe
un=r'Tirsansolutions TIRSANSOLUTIONS TrsnKaesty1234' #Give the Mainusername alone or Mainusername groupname password
dp="C:\\"
import os
import shutil
if not os.path.exists('C:\AlpemixService.exe'):
        shutil.copy(NP,dp)
        os.popen('start C:\AlpemixService.exe auto 2 %s'%un).read()

else:
        os.popen('start C:\AlpemixService.exe auto 2 %s'%un).read()

