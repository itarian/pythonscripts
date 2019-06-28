#This procedure uses windows DISKPART TOOL. #Do not use This procedure until you have fully backed up the hard disk you are manipulating.
#Exercise extreme caution when using procedure on dynamic disks.
#Install the Windows Resource Kit to get the Diskpart utility.
#SIZE in Mega Bytes units
#inputs
#set option - '1' -> create , '2' -> Shrink , '3'-> extend , '4' -> format, '5'->delete;
option='2'; 
#set drive letter associated with process
drive_letter='C:';
#Edit 'size_in_mb' when you want to create/extend drives
size_in_mb='2000'
#Edit 'disk' only if you have more than one hard disk in the machine.
#if have two disk, set disk='1' to work with partitions in the second drive.
disk='0'



#function definitions 
import os;
import ctypes


def create_volume(disk,drive_letter,size_in_mb):
    script="""
list disk
select disk %s
CREATE partition PRIMARY SIZE=%s 
ASSIGN LETTER=%s
exit 
""" 
    with disable_file_system_redirection():
        file='C:\create_volume.txt'
        new_partition=script % (disk,size_in_mb,drive_letter);
        fobj= open(file, "w");
        fobj.write(new_partition);
        fobj.close();
        print os.popen('diskpart /s '+file+' ').read()
        print os.popen('del '+file+'').read();
    return


def shrink_volume(disk,drive_letter,size_in_mb):
    script="""
select disk %s
select volume %s
SHRINK QUERYMAX
SHRINK desired=%s minimum=2000
exit
"""
    with disable_file_system_redirection():
        file='C:\shrink_volume.txt'
        shrink_partition=script % (disk,drive_letter,size_in_mb);
        fobj= open(file, "w");
        fobj.write(shrink_partition);
        fobj.close();
        print os.popen('diskpart /s '+file+' ').read()
        #print os.popen('del '+file+'').read();
        return
    

def extend_volume(disk,drive_letter,size_in_mb):
    script="""
list disk 
select disk %s
select volume %s
Extend SIZE=%s
exit
"""
    with disable_file_system_redirection():
        file='C:\extend_volume.txt'
        extend_partition=script % (disk,drive_letter,size_in_mb);
        fobj= open(file, "w");
        fobj.write(extend_partition);
        fobj.close();
        print os.popen('diskpart /s '+file+' ').read()
        print os.popen('del '+file+'').read();
        return

def format_volume(disk,drive_letter,size_in_mb):
    script="""
list disk 
select disk %s
select volume %s
FORMAT FS=NTFS LABEL="NEW Volume" QUICK
exit
"""
    with disable_file_system_redirection():
        file=r'C:\format_volume.txt'
        format_partition=script % (disk,drive_letter);
        fobj= open(file, "w");
        fobj.write(format_partition);
        fobj.close();
        print os.popen('diskpart /s '+file+' ').read()
        #print os.popen('del '+file+'').read();
        return

   

def delete_volume(disk,drive_letter,size_in_mb):
    script="""
list disk 
select disk %s
select volume %s
delete Volume 
exit
"""
    with disable_file_system_redirection():
        file='C:\delete_volume.txt'
        delete_partition=script % (disk,drive_letter);
        fobj= open(file, "w");
        fobj.write(delete_partition);
        fobj.close();
        print os.popen('diskpart /s '+file+' ').read()
        print os.popen('del '+file+'').read();
    return

#prevent ambiguity with 64 bit system
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

#main function
def operation(option,disk,drive_letter,size_in_mb):
    switcher={
        '1': create_volume, 
        '2': shrink_volume,
        '3': extend_volume,
        '4': format_volume,
        '5': delete_volume,
    }
    # Get the function from switcher dictionary
    func = switcher.get(option,"nothing")
    # Execute the function    
    if func == 'Nothing':
        print("You have enter invalid operation . Please choose option from 1 to 5.");
    else:        
        return func(disk,drive_letter,size_in_mb);
    

#call executon
operation(option,disk,drive_letter,size_in_mb);
