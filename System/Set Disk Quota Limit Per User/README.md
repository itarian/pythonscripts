Please use the script to configure disk quota limit for the specific user - able to set limit and threshold level in bytes.

As an administrator, I want to limit a drive space for a user then I can use this script

usage sample:
you can change the value of following variables as per your requirement,

drName = 'C:' ## Here you can modify your drive name if you want to set drive 'E:'
threshold = '8000000000' ## warning level in bytes - 8GB set for warning
limit = '10000000000' ## limit level in bytes - 10GB set for limit
username = 'newuser' ## username of the specific user
mode = 'track' ## mode has 2 options - track / enforce; when we use track - disk limit can be crossed by the user but we notified when we use enforce user is blocked to cross his limit

Run the script procedure as either "system user" 

This Script run as system User