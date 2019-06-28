Please run the procedure as a System User

The procedure takes the following as a parameter from the user and creates a new daily task in Windows Task Scheduler.

run_as_username='username'
run_as_password='********'
task_name='task name COMODO'
task_run=r'C:\windows\system32\calc.exe'
hour_at=18
minute_at=54

To identify the procedure whether it is run successfully, check the log whether which contains the same message like "SUCCESS: The scheduled task "task name COMODO" has successfully been created." otherwise given the valid value for parameters.

Note:

hour_at parameter will support only 24-hours format, please don't try 12-hours format

Task will be scheduled based on the Local Time of the Windows Endpoint

 

run_as_username='username' run_as_password='********' task_name='task name COMODO' task_run=r'C:\windows\system32\calc.exe' hour_at=18 minute_at=54
Procedure's Instructions
