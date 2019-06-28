This Script is Used to creates a shortcut on the public users desktop that points to internet explorer

1. Download an icon file from an internet URL if we so desire (make it easy to comment out if we do not need that)
2. Creates a shortcut file in c:\users\public\desktop (Windows 7 and above) and allows us to easily change the icon to a file of our choosing
3. Shortcut should point to C:\Program Files (x86)\Internet Explorer\iexplore.exe (Or whatever path we determine is correct to get to IE) and allow a command line argument of a URL to access such as www.google.com
4. Script should be able to specify an icon file for the shortcut

1.Give the Download icon URL 2.Give the preferred path location 3.Give any icon file name as per your wish Eg: URL='http://www.iconarchive.com/download/i50371/hopstarter/orb/Internet-Explorer.ico' #Give the Download icon URL src_path="C:\Users\win732dt\Downloads\icon" #Give the preferred path location fileName = '1.ico'#Give any icon file name as per your wish
