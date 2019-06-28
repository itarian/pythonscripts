pwd_hash=r"864069d03250a47306ed5abf872cf3d9df796303ebc4ddeed101e07f6b7646de"#provide your pwd_hash value here
disable_if_gw_unreachable=r"yes" #provide your disable_if_gw_unreachable value here
dome_locations_url=r"https://billtrust-swg.cdome.net:17443/" #provide your dome_locations_url value here
pac_file_link=r"https://dome.comodo.com/pac_file/master_63a5952bab8d10954f9dfd0b5be9dc85?lcid=198"# provide your pac_file_link value here
preshared_key=r"Comodo360!" #provide your preshared_key value here
protect_host_file=r"yes" #provide your protect_host_file value here

import _winreg
import sys
import os
import ctypes
import ssl
import shutil

REG_PATH_DOME_SWG_AGENT_32 = r"SOFTWARE\Comodo\Dome Agent\config"
REG_PATH_DOME_SWG_AGENT_64 = r"SOFTWARE\Wow6432Node\Comodo\Dome Agent\config"
REG_KEY_ROOT = _winreg.HKEY_LOCAL_MACHINE
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

        
def set_reg(root, path, name, value):
    try:
        _winreg.CreateKey(root, path)
        registry_key = _winreg.OpenKey(root, path, 0, _winreg.KEY_WRITE)
        _winreg.SetValueEx(registry_key, name, 0, _winreg.REG_SZ, value)
        _winreg.CloseKey(registry_key)
        print str(path) + " " + str(name) + " has been updated with " + str(value)
        return True

    except WindowsError:
        print "Problem occured while trying to set registry : " + str(path) + " " + str(name)

        return False
def update_swg_config1(reg_path):
    set_reg(REG_KEY_ROOT, reg_path, "pwd-hash", "%s"%(pwd_hash))


def update_swg_config(reg_path):

        set_reg(REG_KEY_ROOT, reg_path, "disable-if-gw-unreachable", "%s"%(disable_if_gw_unreachable))
        set_reg(REG_KEY_ROOT, reg_path, "dome-locations-url", "%s"%(dome_locations_url))
        set_reg(REG_KEY_ROOT, reg_path, "pac-file-link", "%s"%(pac_file_link))
        set_reg(REG_KEY_ROOT, reg_path, "preshared-key", "%s"%(preshared_key))
        set_reg(REG_KEY_ROOT, reg_path, "protect-host-file", "%s"%(protect_host_file))
        set_reg(REG_KEY_ROOT, reg_path, "pwd-hash", "%s"%(pwd_hash))
with disable_file_system_redirection():
    a=os.popen('wmic product where "Name like "%Dome%"" get Name').read()
    if "Dome" in a:
        print "Comodo Dome Agent already exists in Endpoint"
        if os.path.exists("C:\Program Files (x86)"):
            update_swg_config1(REG_PATH_DOME_SWG_AGENT_64)
        else:
            update_swg_config1(REG_PATH_DOME_SWG_AGENT_32)
        
            
    else:
        
        def c1temp():
            temp=os.environ['PROGRAMDATA']+'\c1_temp'
            if os.path.exists(temp):
                pass
            else:
                os.mkdir(temp)
            return(temp)

        temp=c1temp()

        def Download(Path, URL, FileName, Extension):
            import urllib2
            import os
            fn = FileName+Extension
            fp = os.path.join(Path, fn)
            request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
            try:
                gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
                parsed = urllib2.urlopen(request,context=gcontext)
            except:
                parsed = urllib2.urlopen(request)
            with open(fp, 'wb') as f:
                while True:
                    chunk=parsed.read(100*1000*1000)
                    if chunk:
                        f.write(chunk)
                    else:
                        break
                return fp
            return False

        def wincmd(command):
            import ctypes
            from subprocess import PIPE, Popen
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
                obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
                out, err = obj.communicate()
                ret= obj.returncode
                if ret == 0:
                    return(out)
                return False   

        cdome_url=r'https://s3.amazonaws.com/domeagent/cDomeAgent.msi'

        print 'Configure and Install Dome SWG Agent Procedure started'

        print "Update/Set SWG Agent Config"



        print 'Downloading Dome SWG Agent from ' + cdome_url

        fp=Download(temp,cdome_url,'CdomeAgent',r'.msi')

        if fp:
            print 'Dome SWG Agent installation  begins'
            print wincmd('msiexec /i  '+fp+'  /qn')
        else:
            print 'Dome SWG Agent failed to dowload. Please check link ' + cdome_url + 'is uptodate'
            sys.exit()

        # Set Agent config for 32 and 64 bit windows PCs
        if os.path.exists("C:\Program Files (x86)"):
            update_swg_config(REG_PATH_DOME_SWG_AGENT_64)
        else:
            update_swg_config(REG_PATH_DOME_SWG_AGENT_32)
        

        
        print "Configuration Completed"

        print 'Configure and Install Dome SWG Agent Procedure completed'

