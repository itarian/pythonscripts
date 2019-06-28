folder = r"C:\Users\Administrator.W10P64\Downloads"
import os
folder_size=0
if os.path.isdir(folder):
    for(path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)
    print "Size of the Directory %s %s %s MB" %(folder, '.'*20, round(folder_size/(1024*1024.0), 2))
else:
    print('Please provide the valid directory path')
