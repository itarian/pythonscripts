#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
appName=itsm.getParameter('parameterName') 
import subprocess
process=subprocess.Popen(['taskkill', '/t', '/f', '/im', '%s'%(appName)], shell=True, stdout=subprocess.PIPE)
result=process.communicate()[0]
print result
