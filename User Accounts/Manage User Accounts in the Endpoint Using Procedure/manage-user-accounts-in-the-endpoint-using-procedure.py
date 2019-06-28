option= '13'  # provide option for selecting the operation to perform
#option 1: For creating user provide the uN and pwd
#option 2: For changing the password provide uN and pwd
#option 3: For delete the existing user provide uN
#option 4: For disable the password change provide uN
#option 5: For rename the user account provide uN and newuN
#option 6: For display login detail for a account provide uN
#option 7: For Enabling the account and unlock the account provide uN 
#option 8: For Disabling the account provide uN
#option 9: For enabling the local administrator user account provide uN
#option 10: Enable built in "Administrator" account
#option 11: Disable built in "Administrator" account 
#option 12: For removing user account from administrator group Provide uN
#option 13: For creating a Domain account  provide uN


uN = "Lava24"
pwd= 'Comodo@1234'
newuN="Rain"

import ctypes
import subprocess
import os


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
			
def changepwd(uN,pwd):
    with disable_file_system_redirection():
        disablepwd=' net user ' +uN+' '+pwd+' /Passwordchg:Yes'
        disable=os.popen(disablepwd).read()
        print disable
        print "The password has been changed for the user " + uN
        

def createuser(uN,pwd):
    with disable_file_system_redirection():
        AddUser= 'net user ' +uN+' '+pwd+ ' /add /passwordreq:yes'
        Createusr=os.popen(AddUser).read()
        print Createusr
        print "The user " + uN + " has been created successfully"


def disablepwd(uN):
    with disable_file_system_redirection():
        d='net user ' +uN+' /Passwordchg:no'
        disable=os.popen(d).read()
        print disable
        print "The user " + uN + " cannot able to change password"

def deleteuser(uN):
    with disable_file_system_redirection():
        Deleteusr= 'net user ' +uN+' /delete'
        Delete=os.popen(Deleteusr).read()
        print Delete
        print "The user " + uN + " has been deleted successfully"
		

def renameusr(uN,newuN):
    with disable_file_system_redirection():
        rename= "wmic useraccount where name="+"'"+uN+"'"+" rename " +newuN
        renameusr=os.popen(rename).read()
        print renameusr
        print "The user name " + newuN + " has changed"

def login(uN):
    with disable_file_system_redirection():
        login= 'net user ' +uN+ ' | findstr /C:"Last logon"'
        loginuser=os.popen(login).read()
        print "The login details for " + uN + ':'  ' ' + loginuser

def enable(uN):
    with disable_file_system_redirection():
        enable= 'net user ' +uN + ' /active:yes'
        enableacc=os.popen(enable).read()
        print enableacc
        print 'The account is enabled for ' +uN

def disable(uN):
    with disable_file_system_redirection():
        disable= 'net user ' +uN + ' /active:no'
        disableacc=os.popen(disable).read()
        print disableacc
        print 'The account is disabled for ' +uN

def adminacc(uN):
    with disable_file_system_redirection():
        acc= 'net localgroup administrators ' + uN + ' /add'
        adminacc=os.popen(acc).read()
        print adminacc
        print 'The admin account is created for the user ' + uN 

def enableadmin():
    with disable_file_system_redirection():
        enable="net user administrator /active:Yes"
        enableacc=os.popen(enable).read()
        print enableacc
        print "The administrator account is enabled"
        print 'Restarting at the endpoint for applying changes'
        net=os.popen('shutdown -r').read()
        print net

def disableadmin():
    with disable_file_system_redirection():
        enable='net user administrator /active:no'
        enableacc=os.popen(enable).read()
        print enableacc
        print "The administrator account is disabled"
        print 'Restarting at the endpoint for applying changes'
        net=os.popen('shutdown -r').read()
        print net


def removeadmin(uN):
    with disable_file_system_redirection():
        removeacc='net localgroup administrators ' + uN + ' /delete'
        remove=os.popen(removeacc).read()
        print remove
        print 'Admin access changed for the user ' + uN
        
def domainuser(uN):
    with disable_file_system_redirection():
        Dmuser= 'net user ' +uN+' /add domain /passwordreq:yes'
        Dmusr=os.popen(Dmuser).read()
        print Dmusr
        print "The user " + uN + " has been created successfully"


        
if option == '1':
    createuser(uN,pwd)
elif option == '2':
    changepwd(uN,pwd)
elif option == '3':
    deleteuser(uN)
elif option == '4':
    disablepwd(uN)
elif option == '5':
    renameusr(uN,newuN)
elif option == '6':
    login(uN)
elif option == '7':    
    enable(uN)
elif option == '8':
    disable(uN)
elif option == '9':
    adminacc(uN)
elif option == '10':
    enableadmin()
elif option == '11':
    disableadmin()    
elif option == '12':
    removeadmin(uN)
elif option == '13':
    domainuser(uN)


else:
    print 'Selected option does not exist'
