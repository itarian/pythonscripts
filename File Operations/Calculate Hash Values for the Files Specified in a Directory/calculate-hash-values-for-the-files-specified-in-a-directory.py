directory=r"C:\Users\Peacock\Downloads"#mention your directory here
option='3' # provide option for selecting the operation to perform
#option 1: For Calculating Hash value for a directory using Sha256
#option 2: For Calculating Hash value for a directory using Sha1
#option 3: For Calculating Hash value for a directory using MD5

import hashlib
import os

def file_hash_md5(filename):
  h = hashlib.md5()
  with open(filename, 'rb', buffering=0) as f:
    for b in iter(lambda : f.read(128*1024), b''):
      h.update(b)
  return h.hexdigest()

def file_hash_sha1(filename):
    h = hashlib.sha1()
    with open(filename, 'rb', buffering=0) as f1:
        for b in iter(lambda : f1.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

def file_hash_sha256(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f1:
        for b in iter(lambda : f1.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

if option == '1':
    print "The files are:"
    for root, dirs, files in os.walk(directory):
        for i in files:
            filepath = os.path.join(root,i)
            print i
            v=str(file_hash_sha256(filepath))
            print "The sha256 value is: "+v

elif option == '2':
    print "The files are:"
    for root, dirs, files in os.walk(directory):
        for i in files:
            filepath = os.path.join(root,i)
            print i
            v=str(file_hash_sha1(filepath))
            print "The sha1 value is: "+v

elif option == '3':
    print "The files are:"
    for root, dirs, files in os.walk(directory):
        for i in files:
            filepath = os.path.join(root,i)
            print i
            v=str(file_hash_md5(filepath))
            print "The md5 value is: "+v

else:
  print "No such option"
  
    
    
    

    
    
