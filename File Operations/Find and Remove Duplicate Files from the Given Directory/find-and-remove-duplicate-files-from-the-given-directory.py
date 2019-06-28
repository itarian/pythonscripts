directory_path=r'C:\Users\root\Downloads'
import os
import hashlib

def hashfile(path, blocksize = 65536):
    try:
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()
    except Exception as e:
        print e

def findDup(parentFolder):
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s %s' %('.'*20, dirName))
        for filename in fileList:
            path = os.path.join(dirName, filename)
            file_hash = hashfile(path)
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups

def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('\nDuplicates found:')
        for result in results:
            for subresult in result:
                print('%s' % subresult)
    else:
        print('\nNo duplicate files found.')

def removeDuplicates(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print '\nRemoved files:'
        for result in results:
            for ele in result[:-1]:

                os.remove(ele)
                print ele
    else:
        pass

dict = findDup(directory_path)
printResults(dict)
removeDuplicates(dict)
