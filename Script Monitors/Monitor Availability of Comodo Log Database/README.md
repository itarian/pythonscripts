Hi, Please use the script for monitor the availability of log database file.
This custom monitoring script will monitor the following steps:

1.It checks whether is cislogs.sdb file is present or not, if it is not present it will raise the alert.
2.If the file exists then it checks the internally DataBase file schema where the all tables having data ie. entries or not, If all the tables entries are empty it will raise the alert.

Plese, refer the below-attached JSON file, and run the script as the system administrator.