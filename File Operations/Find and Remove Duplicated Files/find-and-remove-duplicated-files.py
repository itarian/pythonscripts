## find and remove duplicate files, not by name. by content!
import os
import ctypes
import hashlib
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
with disable_file_system_redirection():
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
        # Dups in format {hash:[names]}
        dups = {}
        for dirName, subdirs, fileList in os.walk(parentFolder):
            print('Scanning %s...' % dirName)
            for filename in fileList:
                # Get the path to the file
                path = os.path.join(dirName, filename)
                # Calculate hash
                file_hash = hashfile(path)
                # Add or append the file path
                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
        return dups
    def printResults(dict1):
        results = list(filter(lambda x: len(x) > 1, dict1.values()))
        if len(results) > 0:
            print('Duplicates Found:')
            print('The following files are same. The name could differ, but the content is same')
            print('__')
            for result in results:
                for subresult in result:
                    print('%s' % subresult)
                print('__')
        else:
            print('No duplicate files found.')
    def removeDuplicates(dict1):
        results = list(filter(lambda x: len(x) > 1, dict1.values()))
        if len(results) > 0:
            print '\n'
            print 'Removed Files:'
            print('__')
            for result in results:
                for ele in result[:-1]:
                    os.remove(ele)
                    print ele
                print('__')
        else:
            pass
    if __name__ == '__main__':
        dict = findDup('C:\\Users\\Administrator\\Downloads') ## you change your path here...
        printResults(dict)
        removeDuplicates(dict)
