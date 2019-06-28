import os
import sys
import ctypes
global temp
class disable_file_system_redirection:
    import ctypes
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
       
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

with disable_file_system_redirection():

    temp=os.environ['TEMP']
    path1=temp+'\\disk.txt'
     
    script='''
    list disk
    '''
    f=open(path1,'w+')
    f.write(script)
    f.close()
    os.chdir(temp)
    def showdetails(disk):   
        path2=temp+'\\partitions.txt'   
        script='''
        select disk %s
        detail disk
        '''
        new_script= script % (disk)
        f=open(path2,'w+')
        f.write(new_script)
        f.close()
        os.chdir(temp)
        p=os.popen('diskpart /s "'+path2+'"').readlines()
        parts=0
        for i in range(len(p)):
            if '----------  ---  -----------  -----  ----------  -------  ---------  --------' in p[i]:
                parts=i+1
        if parts==0:
            print 'Disk Details'
            for i in range(0,len(p)):
                print p[i]
            return()
        else:
            partsn=len(p)-parts+1
            for j in range(0,len(p)):
                print p[j]
     
     
        out=[]
        new_disk='select disk %s \n' % (disk)
        out.append(new_disk)
        for i in range(partsn):
            out.append('select volume '+str(i)+'\n')
            out.append('detail volume \n') 
        path3=temp+'\\details.txt'
        f=open(path3,'w+')
        for i in out:
            f.write(i)
        f.close()
        os.chdir(temp)
        q=os.popen('diskpart /s "'+path3+'"').readlines()
        for i in range(0,len(q)):
            print q[i]
     
     
     
    r=os.popen('diskpart /s "'+path1+'"').readlines()
     
    flag=0
     
    for i in range(len(r)):
        if '--------  -------------  -------  -------  ---  ---' in r[i]:
            flag=i+1
     
    diskn=len(r)-flag
     
     
    if diskn==1:
        showdetails(disk=0)
    else:
        for i in range(diskn):
            showdetails(disk=i)
