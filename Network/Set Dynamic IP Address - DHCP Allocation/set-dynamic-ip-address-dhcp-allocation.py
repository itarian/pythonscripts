import os;
import re;
import ctypes
file='C:\\automateip.ps1';
input="""
$IPType = "IPv4"
$adapter = Get-NetAdapter | ? {$_.Status -eq "up"}
$interface = $adapter | Get-NetIPInterface -AddressFamily $IPType

If ($interface.Dhcp -eq "Disabled") {
    # Remove existing gateway
    If (($interface | Get-NetIPConfiguration).Ipv4DefaultGateway) {
        $interface | Remove-NetRoute -Confirm:$false
    }

    # Enable DHCP
    $interface | Set-NetIPInterface -DHCP Enabled

    # Configure the  DNS Servers automatically
    $interface | Set-DnsClientServerAddress -ResetServerAddresses
}"""

fobj=open(file,"w");
fobj.write(input);
fobj.close();

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
    out=os.popen(r'powershell.exe -executionpolicy bypass -file C:\automateip.ps1').read();
    print(out);

os.remove("C:\\automateip.ps1")
