import _winreg

def main():    
    key = r'HKEY_LOCAL_MACHINE\SOFTWARE\COMODO'
    hekey = key.split('\\')[0]
    hkey = getattr(_winreg, hekey)
    skey = '\\'.join(key.split('\\')[1:])
    try:
        pkey = _winreg.OpenKey(hkey, skey)
        print 'Success: '+hekey+'\\'+skey+' is available'
    except WindowsError as e:
##        print e
        print 'Check whether '+hekey+'\\'+skey+' is valid or accessible!'
        
if __name__ == '__main__':
    main()
