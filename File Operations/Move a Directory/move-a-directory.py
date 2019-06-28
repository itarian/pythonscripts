folder_to_move = r'C:\Program Files\Internet Explorer'
new_folder = r"C:\Users\Administrator.W10P64\Desktop\New"

import shutil
try:
    shutil.copytree(folder_to_move, new_folder)
    print("%s is mvoed into %s"%(folder_to_move, new_folder))
except Exception as err :
    print err
