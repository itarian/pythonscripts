import _winreg

def main():
    ## Pass the here at "key" variable
    key = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft'
    hekey = key.split('\\')[0]
    hkey = getattr(_winreg, hekey)
    skey = '\\'.join(key.split('\\')[1:])
    try:
        pkey = _winreg.OpenKey(hkey, skey)
        print 'Given Key: '+hekey+'\\'+skey
        try:
            print 'Sub Keys: '
            print('-'*25)
            i=0
            while True:
                print _winreg.EnumKey(pkey, i)
                i += 1
        except WindowsError as e:
            pass
        finally:
            try:
                print 'Values: '
                print('-'*25)
                j=0
                while True:
                    sep = ''
                    for k in list(_winreg.EnumValue(pkey, j)):
                        sep = sep+str(k)+'\t'
                    print sep
                    j += 1
            except WindowsError as e:
                pass
    except WindowsError as e:
        print 'Check whether '+hekey+'\\'+skey+' is valid or accessible!'
        
if __name__ == '__main__':
    main()
