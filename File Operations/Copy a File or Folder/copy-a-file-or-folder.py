import os,shutil
source="C:\\Users\\fortnite\\Desktop\\LGPO\\LGPO.exe"
dest="C:\\"
print 'SCRIPT FOR COPYING FILE OR FOLEDER FROM THE SOURCE "%s" TO THE DESTINATION "%s"\n'%(source,dest)

if os.path.exists(source):
    if os.path.isdir(source):
        print("\t*) You are trying to copy the Directory:")
        for root, dirs, files in os.walk(source):
            if not os.path.isdir(root):
                os.makedirs(root)
            for file in files:
                rel_path = root.replace(source, '').lstrip(os.sep)
                dest_path = os.path.join(dest, rel_path)
                if not os.path.isdir(dest_path):
                    os.makedirs(dest_path)
                shutil.copyfile(os.path.join(root, file), os.path.join(dest_path, file))
        print '\t\t*) FOLEDER COPIED SUCCESSFULLY TO THE DESTINATION "%s"'%dest
    elif os.path.isfile(source):
        print("\t*) You are trying to copy the File:")
        shutil.copy2(source,dest)
        print '\t\t*) FILE COPIED SUCCESSFULLY TO THE DESTINATION "%s"'%dest
        

else:
    print 'ERROR FROM THE  SOURCE PATH"%s"'%(source)
