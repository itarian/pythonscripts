folder_path=r"C:\Users\Administrator.W10P64\Desktop\Hia"

import shutil
try:
    shutil.rmtree(folder_path)
    print("%s is removed successfully"%folder_path)
except Exception as err :
    print err
