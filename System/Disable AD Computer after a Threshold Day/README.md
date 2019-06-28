Hi,

This script will disable the AD Computer if the login time of the computer exceeds after threshold specified days (i.e, 15 days). If the threshold day reaches a certain value (30 days) this will trigger auto-remediation script for removing the specified computer.

i.e, For Example:

value='15' # Provide the days to disable the account
rem_value='30' # Provide the days to remove the account

Note:

Run as a Custom Monitoring Script.

https://wiki.itarian.com/frontend/web/topic/how-to-use-custom-script-procedure-monitoring

Configure the following script as an Auto-remediation to remove the AD computer account,

"Remove AD User after a threshold day"

https://scripts.itarian.com/frontend/web/topic/remove-ad-computer-after-a-threshold-day