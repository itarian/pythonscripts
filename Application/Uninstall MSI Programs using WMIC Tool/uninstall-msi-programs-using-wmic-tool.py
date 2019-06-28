#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
proName=itsm.getParameter('parameterName') 
import os
out=os.popen('wmic product where name="%s" call uninstall'%(proName)).read()
print(out)
