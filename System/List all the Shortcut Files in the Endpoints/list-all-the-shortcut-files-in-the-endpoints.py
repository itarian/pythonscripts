def list_device_shortcut():
    import os
    import ctypes
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
        script=r"""

        $strComputer = "." 

       $colItems = get-wmiobject -class "Win32_ShortcutFile" -namespace "root\CIMV2" `
       -computername $strComputer  

        foreach ($objItem in $colItems) {
            write-host "FileName:" $objItem.name
            write-host "Hidden State": $objItem.Hidden
            write-host "Readable" $objItem.Readable
            write-host "Writeable: " $objItem.Writeable
            write-host 
               } 
             """

        path =os.environ['TEMP']
        file = path+'\\'+'Desktop_setting_details.ps1'
        fobj= open(file, "w");
        fwrite=fobj.write(script);
        fobj.close();
        setpolicy=os.popen('powershell "Set-ExecutionPolicy -ExecutionPolicy Unrestricted" ').read();
        print(setpolicy);
        command ="powershell "+file
        run=os.popen(command).read();
        print("The shortcuts in a device are listed below \n")
        print(run)

    return

list_device_shortcut()
