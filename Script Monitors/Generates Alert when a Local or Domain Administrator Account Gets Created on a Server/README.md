The following script is for monitoring condition that alerts when a local or domain administrator account gets created on a server.

Note:

Run the script as monitoring script.
First time when the script runs it will generate a text file to save the "domain users" u already have in the name of default users.
In the first time a new file will get generated with a low kb value around 1 to 10 kb which contains the user values to compare.
Next time when you run the script another file get created and the contents of the files get compared and the new user added is displayed. 
Whenever a new user is added an alert will get generated.