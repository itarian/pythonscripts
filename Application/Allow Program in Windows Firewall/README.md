Hi,

This script  will allow the program in windows firewall


Steps to follow:

1.you have to pass the path and name in the parameter section.
Refer the wiki to run the procedure with parameters
https://wiki.comodo.com/frontend/web/topic/how-to-create-and-run-procedures-with-parameters

NOTE:
1.Enter_the_path:
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter_the_path"

2..Enter_the_rule:
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter_the_rule"

For example:

path="C:\Program Files\Mozilla Firefox\firefox.exe"#Please mention the file path of the program needed to be allowed
name="allow"#Provide any rule name 

TESTED PLATFORM:

 Windows: 10, 8.1, 8, 7.

Run the script as system user
