Hi, Please refer the script to START, STOP, PAUSE, RESUME, RESTART, DISABLE(a service that can't be started), DEMAND(a service that must be manually started (the default))THE SERVICES, and add\remove programs to startup list

It also added the programs to the startup list to your system. In, if you are added any program, to startup list you can easily remove it from the list. 

1.It will list out the what are the services which are present in your system along with states.(running, stopped, started).

2.It will display the software which is installed in your system.

3.It will list out the what are the startup programs which are present in your system.

If you want to start any services, then added services to the list "start_services=[]" ,ie.start_services=['service name']  ie. start_services=['BDESVC']

like this if u want to stop, pause, resume, restart, disable, demand any service just pass the services name to the list of corresponding services

stop_services=[], restart_services=[], pause_services=[], resume_services=[], serv_demand=[], serv_disabled=[].

Finally, If you want to add startup programs just pass the values in the dictionary format: like ëx={"NAME":""PATH"}.
ex={"Google Chrome":"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe","CCleaner":"C:\Program Files\CCleaner\CCleaner.exe"}
where Google Chrome is the NAME" of the program, and the path is you have to give the (application.exe).

IF U WANT TO REMOVE ANY START UP PROGRAMS JUST GIVE THE NAME OF THE APPLICATION LIKE "Google Chrome"

ie. startup_dele=['NAME'], -> startup_dele=["Google chrome"]