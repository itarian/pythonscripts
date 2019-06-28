Please use the script to uninstall all of your blacklisted programs from your endpoint

Note:

    Modify the variable for your list of programs - blacklist=['program_name_1', 'program_name_2']
    Run as System User

Limitation:

    Programs can be removed:
        Inventory can have msi and exe programs, all msi programs can be removed without user interaction but exe programs can be removed without user interaction when only the program has quiet uninstall string.
    Programs can not be removed:
        The exe programs which has no quiet uninstall string, those are not able to be removed without user interaction

 

blacklist=['Manager', 'Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161', 'Microsoft Visual C++ 2015 x64 Additional Runtime - 14.0.23026', 'PDF Architect 5', 'Pidgin', 'VLC media player', 'Microsoft Visual C++ 2015 Redistributable (x86) - 14.0.24215']