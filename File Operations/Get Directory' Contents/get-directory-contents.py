import os
path='C:\\Program files'
try:
    for i in os.listdir(path):            
        print i                                        
except Exception as err:
    print err
