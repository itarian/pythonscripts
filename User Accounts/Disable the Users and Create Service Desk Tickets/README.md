PARAMETERS TO BE EDITED:

user_names=itsm.getParameter('User_Names') # List
apikey=itsm.getParameter('Api_Key') # String
domain=itsm.getParameter('Domain_Name') # String. Domain which is synced with Endpoint manager account.
email=itsm.getParameter('From_Email') # String. Email from where ticket has to create.

This script will disable the user specified in the list. Run as SYSTEM USER
