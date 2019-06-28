import _winreg
import os
from _winreg import *

is_64="Software\\Wow6432Node\\TeamViewer"
is_32="Software\\TeamViewer"

if 'PROGRAMFILES(X86)' in os.environ.keys():
    path=is_64
else:
    path=is_32


    
def getMDACversion(path):
    
    # Open the key and return the handle object.
    hKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, path)
                          
    # Read the value.                      
    result = _winreg.QueryValueEx(hKey, "ClientID")

    # Close the handle object.
    _winreg.CloseKey(hKey)

    # Return only the value from the resulting tuple (value, type_as_int).
    return result[0]

try:
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    k = OpenKey(reg, path)

    if k:
        print "\nTEAM VIEWER is installed in this Endpoint\n"
        client_ID=getMDACversion(path)
        print "Client ID : "+str(client_ID)
        
except:
    print "Please ensure that the Endpoint has TEAM VIEWER INSTALLED"


