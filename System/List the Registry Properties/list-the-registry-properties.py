def Registry_Properties():
    script=r"""
            On Error Resume Next
            strComputer = "."
            Set objWMIService = GetObject("winmgmts:" _
            & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")

            Set colItems = objWMIService.ExecQuery("Select * from Win32_Registry")
            For Each objItem in colItems
              Wscript.Echo "Caption: " &objItem.Caption
              Wscript.Echo "Current Size: " &objItem.CurrentSize
              Wscript.Echo "Description: " &objItem.Description
              Wscript.Echo "Installation Date: " &objItem.InstallDate
              Wscript.Echo "Maximum Size: " &objItem.MaximumSize
              Wscript.Echo "Name: " &objItem.Name
              Wscript.Echo "Proposed Size: " &objItem.ProposedSize
              Wscript.Echo "Status: " &objItem.Status
              Next

        }"""

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
            import os
            path =os.environ['TEMP']
            file = path+'\\'+'Registry_Properties.vbs'
            fobj= open(file, "w");
            fwrite=fobj.write(script);
            fobj.close();
            run=os.popen('cscript.exe '+file).read();
            print(run)
            try:
                os.remove(file)
            except OSError:
                pass
    return

Registry_Properties()
