import _winreg as winreg
import itertools

def enumerate_serial_ports():
    """ Uses the Win32 registry to return an
        iterator of serial (COM) ports
        existing on this computer.
    """
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        for i in itertools.count():
            try:
                val = winreg.EnumValue(key, i)
                print  str(val[1])
            except WindowsError:
                break

    except WindowsError:
        print "Serials port keys are not present in Registry"

    
enumerate_serial_ports()
