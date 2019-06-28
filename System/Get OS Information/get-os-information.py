import os
print os.popen('systeminfo | findstr /B /C:"OS "').read()
