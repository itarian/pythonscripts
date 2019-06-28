dir_name = "C:\Python27"  #Provide Your Folder Path
File_extension=r".py"     #Provide Your File Extension

import os

test = os.listdir(dir_name)
for item in test:
    if item.endswith(File_extension):
        print (os.path.join(dir_name, item))
