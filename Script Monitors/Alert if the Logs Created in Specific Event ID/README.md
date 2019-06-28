Hi

Please use this script to track specific event Id and get details when the event occurs.
The script will check the event logs for every 15 min by default. Whenever the event happened, an alert will be generated. 
Input:

Eventid = Mention the Event ID to get the log details

Mins=15  Mention the minutes to check the crashed files (It should be same as monitoring time period) 

Example:

     Eventid=1002

    Mins=15

Note:

This script as Custom Monitoring script. Please refer https://wiki.comodo.com/frontend/web/topic/how-to-use-custom-script-procedure-monitoring

And set the custom Monitoring condition duration as 15 min

 

This script run as a custom monitoring script