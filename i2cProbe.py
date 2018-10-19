#!/usr/bin/python3

import rebootServers
import hs_session
from pexpect import pxssh
import threading
import time

threads = []

servers = [
    '10.0.2.165',
    '10.0.2.168'
]
cycle = 1

def server_ident(server, logNum):
    user = 'root'
    passwd = 'root'
    print ('{} Reboot Server {}'.format(logNum,server))
    rebootServers.reboot(cycle,logNum,server)
    time.sleep(90)
    print ('{} Login to {} '.format(logNum,server))
    session = pxssh.pxssh()
    hs_session.login(session,server,user,passwd)
    command = 'SysManComm on'
    hs_session.power_ctl(cycle,logNum,session,server,command)
    time.sleep(120)
    hs_session.create_record(cycle,logNum,session,server)
    hs_session.get_available_cards(cycle,logNum,session,server)
    command = 'SysManComm off'
    hs_session.power_ctl(cycle, logNum, session, server, command)
    time.sleep(30)

if __name__ == '__main__':
    logNum = 0
    while True:
        cycle = cycle + 1
        for server in servers:
            logNum = logNum + 1
            t = threading.Thread(name = 'Server Thread', target = server_ident, args = (server, logNum))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        time.sleep(2)
        logNum = 0
