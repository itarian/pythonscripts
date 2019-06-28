Hi,

This script will disable the AD user if the login time of the user exceeds after threshold specified days (i.e, 15 days). 
If the threshold day reaches a certain value (i.e, 30 days) this will trigger auto-remediation script for removing the specified AD User.

i.e, For Example:


value='15' # Provide the days to disable the AD user account

rem_value='30' # Provide the days to remove the AD user account

Note:

Run as a Custom Monitoring Script.

https://wiki.itarian.com/frontend/web/topic/how-to-use-custom-script-procedure-monitoring

Configure the following script as an Auto-remediation to remove the AD user account,


"Remove AD User after a threshold day"

https://scripts.itarian.com/frontend/web/topic/remove-ad-user-after-a-threshold-day