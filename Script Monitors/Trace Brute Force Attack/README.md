This script is used to create an alert after x number of logon failures.Generally in an brute force attack n number of log on failures may occur there are no specific count for it. It's to be noted that logon failures may also occur in other cases too ex:user provided wrong user name or password.In this script the user has been provided an option to create a alert after specific number of log on failures according to their wish.

NOTE:

Editable Parameters:

no=10 ##Mention the no of log on failures after which the alert should be generated(It has been set to a default 10 the user can change according to their requirement).

Mins=2 ##Here mention the minutes to check for the logon failures (It should be same as monitoring time period)

Please run this script as custom monitoring script