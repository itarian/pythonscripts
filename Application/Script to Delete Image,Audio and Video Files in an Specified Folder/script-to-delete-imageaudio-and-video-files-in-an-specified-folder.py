OPTION=2 # Provide 1 if you want to delete image files from the folder
         # Provide 2 if you want to delete audio files from the folder
         # Provide 3 if you want to delete video files from the folder

dir = r"C:\Users\rainbow\Desktop" # Provide Path to the folder

import glob
import os
if OPTION==1:
    print "Deleting Image Files" 
    list1=[r'*.bmp',r'*.dib',r'*.bpg',r'*.jpg',r'*.jpeg',r'*.jpe',r'*.jif',r'*.jfif',r'*.jfi',r'*.gif',r'*.png',r'*.tiff',r'*.tif']
    for i in range(0,len(list1)):
        for path in glob.iglob(os.path.join(dir, list1[i])):
            os.remove(path)
if OPTION==2:
    print "Deleting Audio Files" 
    list1=[r'*.3gp',r'*.aiff',r'*.m4a',r'*.m4p',r'*.mp3',r'*.raw',r'*.wav',r'*.wma',r'*.webm']
    for i in range(0,len(list1)):
        for path in glob.iglob(os.path.join(dir, list1[i])):
            os.remove(path)
if OPTION==3:
    print "Deleting Video Files" 
    list1=[r'*.webm',r'*.mkv',r'*.flv',r'*.avi',r'*.gif',r'*.wmv',r'*.mp4',r'*.mpeg',r'*.3gp']
    for i in range(0,len(list1)):
        for path in glob.iglob(os.path.join(dir, list1[i])):
            os.remove(path)

    
    
