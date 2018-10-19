import os

serverlist = [
    {'server': '10.0.2.165','powerPort':'22','powerBar':'10.0.2.115'},
    {'server': '10.0.2.149','powerPort':'11','powerBar':'10.0.2.117'},
    {'server': '10.0.2.189','powerPort':'13','powerBar':'10.0.2.117'},
    {'server': '10.0.2.208','powerPort':'3','powerBar':'10.0.2.116'},
    {'server': '10.0.2.131','powerPort':'12','powerBar':'10.0.2.116'},
    {'server': '10.0.2.134','powerPort':'22','powerBar':'10.0.2.116'},
    {'server': '10.0.2.180 ','powerPort':'11','powerBar':'10.0.2.115'},
    {'server': '10.0.2.189 ','powerPort':'12','powerBar':'10.0.2.115'},
    {'server': '10.0.2.189 ', 'powerPort': '13', 'powerBar': '10.0.2.115'},
    {'server': '10.0.2.168 ', 'powerPort': '16', 'powerBar': '10.0.2.115'},
    {'server': '10.0.2.168 ', 'powerPort': '23', 'powerBar': '10.0.2.115'}
]

oid = '.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.'

def reboot(cycle, logNum, server):
    for target in serverlist:
        if server in target.get('server'):
            print ('Cycle {} {} Reboot power to {} with snmpset -v 2c -c public {} {}{} -i 3 '.format(cycle,logNum, server,target.get('powerBar'),oid,target.get('powerPort')))
            powerBar = target.get('powerBar')
            powerPort = target.get('powerPort')
            os.system('snmpset -v 2c -c private {} {}{} i 3'.format(powerBar,oid,powerPort))