File = 'C:\Users\Akita\Downloads\patch_agent.msi'  ## you can change your path here...

## to get MD5 and SHA1 checksum value
import hashlib
BLOCKSIZE = 65536
hasher = hashlib.md5()

print 'given file: {}'.format(File)
with open(File, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
print 'MD5 checksum: {}'.format(hasher.hexdigest())
hasher = hashlib.sha1()
with open(File, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
print 'SHA1 checksum: {}'.format(hasher.hexdigest())
'''
usage:
to verify the file whether completely transfered or not
to verify the file after download from internet if they given MD5 or SHA1
to compare files
'''
