Hi,

This script will help to download and install any application from url.

Steps to follow:

1.you have to pass the url and silent command in the parameter section.
Refer the wiki to run the procedure with parameters
https://wiki.comodo.com/frontend/web/topic/how-to-create-and-run-procedures-with-parameters

NOTE:
1.Enter_the_URL:
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter your URL"

2..Enter_the_silent_command:
 TYPE: String
 EM LABEL: Any name
 Default value: "Enter the silent command"
 

For example:

URL = r'https://onedrive.live.com/download?cid=A910C8EF113350FB&resid=A910C8EF113350FB%21116&authkey=AOfmMyN4yDuVkXU'

silent="/S"'
 

TESTED PLATFORM:

 Windows: 10, 8.1, 8, 7.

Run as System User
