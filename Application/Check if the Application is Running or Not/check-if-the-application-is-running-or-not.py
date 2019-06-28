#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name

appName =itsm.getParameter('parameterName')
import os
def IsAppRunning(appName):
    proObj = os.popen('TASKLIST /FI "STATUS eq running"')
    runApps = proObj.read()
    return appName in runApps

if IsAppRunning(appName):
    print 'Success: '+appName+' is running'
else:
    print 'Fail: '+appName+' is not running'
