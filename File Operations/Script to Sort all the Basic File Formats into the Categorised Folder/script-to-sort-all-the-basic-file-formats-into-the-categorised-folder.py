dir_name = "C:\\Users\\comodo\\Desktop"  #Provide Your Folder Path

import os
import shutil

p=dir_name+"\\Excel"
q=dir_name+"\\Word"
r=dir_name+"\\Powerpoint"
s=dir_name+"\\PDF"
t=dir_name+"\\Pictures"
u=dir_name+"\\Movies"
v=dir_name+"\\Files"
w=dir_name+"\\Music"

test = os.listdir(dir_name)
if test==[]:
    print "There are no files in the specified folder "+dir_name
else:
    if not os.path.exists(p):
        os.mkdir(p)
    if not os.path.exists(q):
        os.mkdir(q)
    if not os.path.exists(r):
        os.mkdir(r)
    if not os.path.exists(s):
        os.mkdir(s)
    if not os.path.exists(t):
        os.mkdir(t)
    if not os.path.exists(u):
        os.mkdir(u)
    if not os.path.exists(v):
        os.mkdir(v)

    for item in test:
        if item.endswith('.xls'):
            a= (os.path.join(dir_name, item))
            shutil.move(a,p)
            print (a+" file is sorted successfully in a folder Excel")
        if item.endswith('.doc') or item.endswith('.docx'):
            b= (os.path.join(dir_name, item))
            shutil.move(b,q)
            print (b+" file is sorted successfully in a folder Word")
        if item.endswith('.ppt') or item.endswith('.pptx'):
            c= (os.path.join(dir_name, item))
            shutil.move(c, r)
            print (c+" file is sorted successfully in a folder Powerpoint")
        if item.endswith('.pdf'):
            d= (os.path.join(dir_name, item))
            shutil.move(d,s)
            print (d+" file sorted successfully in a folder PDF")
        if item.endswith('.jpg') or item.endswith('.jpeg') or item.endswith('.bmp') or item.endswith('.png') or item.endswith('.gif') or item.endswith('.tiff'):
            e= (os.path.join(dir_name, item))
            shutil.move(e,t)
            print (e+" file is sorted successfully in a folder Picture")
        if item.endswith('.avi') or item.endswith('.mp4') or item.endswith('.mov'):
            f= (os.path.join(dir_name, item))
            shutil.move(f,u)
            print (f+" file is sorted successfully")
        if item.endswith('.mp3') or item.endswith('.wav') or item.endswith('.wma'):
            g= (os.path.join(dir_name, item))
            shutil.move(g,w)
            print (g+" file is sorted successfully in a folder Music")
        if item.endswith('.exe') or item.endswith('.msi') or item.endswith('.zip') or item.endswith('.rar') or item.endswith('.7z') or item.endswith('.sh') or item.endswith('.bat') or item.endswith('.iso') or item.endswith('.txt'):
            h= (os.path.join(dir_name, item))
            shutil.move(h, v)
            print (h+" file is sorted successfully in a folder Files")

    print ("Thus all the files are sorted successfully in the appropriate folders")
