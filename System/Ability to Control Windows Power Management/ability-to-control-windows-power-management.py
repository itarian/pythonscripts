import os
option='1'
##Enter option '0' for Balanced state.
##Enter option '1' for POWER SAVER state.
##Enter option '2' for HIGH PERFORMANCE state.
POW_STATES={'1':'powercfg.exe /setactive 381b4222-f694-41f0-9685-ff5bb260df2e','2':'powercfg.exe /setactive a1841308-3541-4fab-bc81-f71556f20b4a','3':'powercfg.exe /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'}
os.popen(POW_STATES.values()[int(option)]).read()
if option=='0':
    print 'POWER PLAN HAS BEEN CHANGED TO "Balanced"'
elif option=='1':
    print 'POWER PLAN HAS BEEN CHANGED TO "POWER SAVER"'
elif option=='2':
    print 'POWER PLAN HAS BEEN CHANGED TO "HIGH PERFORMANCE"'
else:
    print 'Please give the desired option.'
