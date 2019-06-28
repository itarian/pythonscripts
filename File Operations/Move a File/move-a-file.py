file_path=r"C:\Users\Administrator.W10P64\Downloads\pythonver.bat"
destination_path=r"C:\Users\Administrator.W10P64\Desktop"

import shutil
try:
    shutil.move(file_path, destination_path)
    print("%s is moved to %s"%(file_path, destination_path))
except Exception as err :
    print err
