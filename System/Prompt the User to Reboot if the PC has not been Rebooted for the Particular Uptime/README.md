Note:
you can set any number of days that the up time of the system on the first line of code
Example: days=14

Explanation:
Case 1:
If the system is pending to restart after windows update is complete,
Alert message occurs and Execution log at IT Service Management (ITSM) would be

Date and Time: 16/02/2018 10:34
Machine Info: BOND-PC - 10.108.57.168

--------------------------------------------------------------------------------------------------------

The following alert message is sent to the user "root"
Please reboot your system! Because the system was not restarted after the windows update was completed.
 

Case 2:
If the system is not pending to restart but the system up time is more than 14 days (days can be modified),
Alert message occurs, and the Execution log at the ITSM would be,

Date and Time: 16/02/2018 10:37
Machine Info: BOND-PC - 10.108.57.168
----------------------------------------
The following alert message is sent to the user "bond"
Please reboot your system! Because your system has not had a fresh startup in 0 days.

Note: For testing purpose I have set days=0 and also the same has been replicated on alerts and logs
 

Case 3:
The system has no pending restart and has the less number of up time in days,

No alert message is sent to the user

And the Execution log at the ITSM would be,

Date and Time: 16/02/2018 10:34
Machine Info: BOND-PC - 10.108.57.168
----------------------------------------
No alert is sent to the user. Because, 

The system uptime is only 0 days.
And It has no pending restart as well.

This script is used to Prompt the user to reboot If the PC has not been rebooted for the particular uptime.Run the script as logged in user.