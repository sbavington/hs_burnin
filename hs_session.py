
import os

def login(session,server,user, passwd):
    try:
        session.login(server,user,passwd)

    except Exception as ex:
        print (ex)

def power_ctl(cycle,logNum,session,server,command):
    session.sendline(command)
    session.prompt()
    lines = session.before.decode()
    for line in lines.splitlines():
        print ('Cycle {} Server {} {} {}'.format(cycle,logNum,server,line))

def create_record(cycle,logNum,session,server):
    print ('If a record file does not exist create one')
    if os.path.exists('static_record.txt'):
        print ('File Exists')
    else:
        print('Create the Static Record File')
        open('static_record.txt','a')

def get_available_cards(cycle,logNum,session,server):
    print ('Scan for Avaliable Cards')
    commands = [
        {'command':'mmi_route','wait': 0}
    ]

    for command in commands:
        send_command = command.get('command')
        session.sendline(send_command)
        session.prompt()
        lines = session.before.decode()
        linecards = []
        pods = []
        for line in lines.splitlines():
            #print ('{} {} {} {}'.format(cycle,logNum,server,line))
            if 'chassis=1 board=2' in line:
                linecards.append('0')
            if 'chassis=1 board=3' in line:
                linecards.append('1')
            if 'chassis=1 board=4' in line:
                linecards.append('2')
            if 'chassis=1 board=5' in line:
                linecards.append('3')
            if 'chassis=1 board=6' in line:
                linecards.append('4')
            if 'chassis=1 board=7' in line:
                linecards.append('5')
            if 'chassis=1 board=8' in line:
                linecards.append('6')
            if 'chassis=1 board=9' in line:
                linecards.append('7')
            if 'chassis=1 board=10' in line:
                linecards.append('8')
            if 'chassis=1 board=11' in line:
                pods.append('0')
            if 'chassis=1 board=12' in line:
                pods.append('1')
            if 'chassis=1 board=13' in line:
                pods.append('2')
            if 'chassis=1 board=14' in line:
                pods.append('3')
        I2cOp_scan(cycle,logNum,session,server,linecards,pods)


def I2cOp_scan(cycle,logNum,session,server,linecards,pods):
    print ('Scan Available Devices for I2C Operation')
    print ('Scan CMM')
    cmm_commands = [
        'I2cOp rdreg16 /pwrmgmt/cmm 0x00',
        'I2cOp rdregf /pwrmgmt/cmm 0x18'
    ]
    for command in cmm_commands:
        session.sendline(command)
        session.prompt()
        lines = session.before.decode()
        for line in lines.splitlines():
            print (cycle,logNum,server,line.strip())
    print ('Scan Backplane')
    bkpln_commands = [
        'I2cOp rdreg16 /pwrmgmt/smbkpln 0x00',
        'I2cOp rdregf /pwrmgmt/smbkpln 0x18'
    ]
    for command in bkpln_commands:
        session.sendline(command)
        session.prompt()
        lines = session.before.decode()
        for line in lines.splitlines():
            print (cycle,logNum,server,line.strip())
    print ('{} {} {} lineCards = {}'.format(cycle,logNum,server,linecards))
    for linecard in linecards:
        linecard_commands = [
            'I2cOp rdreg16 /pwrmgmt/smbkpln/slot/{} 0x00'.format(linecard),
            'I2cOp rdregf /pwrmgmt/smbkpln/slot/{} 0x18'.format(linecard)
            ]
        for command in linecard_commands:
            session.sendline(command)
            session.prompt()
            lines = session.before.decode()
            for line in lines.splitlines():
                print(cycle,logNum,server,line.strip())
    print ('{} {} {} pods = {}'.format(cycle,logNum,server,pods))
    for pod in pods:
        pod_commands =[
            'I2cOp rdreg16 /pwrmgmt/pod-if/slot/{} 0x00'.format(pod),
            'I2cOp rdregf /pwrmgmt/pod-if/slot/{} 0x18'.format(pod)
            ]
        for command in pod_commands:
            session.sendline(command)
            session.prompt()
            lines = session.before.decode()
            for line in lines.splitlines():
                print(cycle,logNum,server,line.strip())