#!/usr/bin/python3
import time
import datetime
import logger
from pexpect import pxssh
def Login(lognum,session,server,port,user,passwd):
    try:
        print ('\n\n=================={:4d}\t{:15s}\t{}\t\tLogin ======================\n'.format(lognum,server,datetime.date.today()))
        session.login (server, 'root',port = port ,password = passwd)

    except Exception as ex:
        template = "A Login exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        print ('{:4d}\t{:15s}\t{}\t{}\t\tLogin Failed!'.format(lognum,server,port,datetime.date.today(),ex))

def sessionCommand(logNum,server,session,command,wait = 1,
                   podSlotsPopulated = [],
                   linecardSlotsPopulated = [],
                   memlinecardPorts = [],
                   mempodPorts = []):
    try:
        if command is None:return
        session.sendline(command)
        session.prompt()
        lines = session.before.decode()
        #print ('{:4d}\t{:15s}\t{:16.5f}\t{}'.format(logNum,server,time.time(),command))
        for line in lines.splitlines():
            print ('{:4d}\t{:15s}\t{:16.5f}\t{}'.format(logNum,server,time.time(),line))
            if 'Timeout waiting for response' in line:
                print ('{:4d}\t{:15s}\t{:16.5f} reboot Timeout  MMI response'.format(logNum,server,time.time()))
                errorLog = '{:4d}\t{:15s}\t{:16.5f} reboot Timeout  MMI response'.format(logNum,server,time.time())
                logger.logError(logNum,server,errorLog)
                session.sendline('reboot')
                time.sleep(2)
                exit()
            if 'Failed to power up' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tFailed to power up reboot '.format(logNum,server,time.time()))
                errorLog = '{:4d}\t{:15s}\t{:16.5f}\tFailed to power up rebooting '.format(logNum,server,time.time())
                logger.logError(logNum, server, errorLog)
                session.sendline('reboot')
                time.sleep(2)
                exit()
            if 'chassis=1 board=2' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 2 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2202')
                memlinecardPorts.append('2')
            if 'chassis=1 board=3' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 3 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2203')
                memlinecardPorts.append('3')
            if 'chassis=1 board=4' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 4 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2204')
                memlinecardPorts.append('4')
            if 'chassis=1 board=5' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 5 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2205')
                memlinecardPorts.append('5')
            if 'chassis=1 board=6' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 6 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2206')
                memlinecardPorts.append('6')
            if 'chassis=1 board=7' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 7 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2207')
                memlinecardPorts.append('7')
            if 'chassis=1 board=8' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 8 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2208')
                memlinecardPorts.append('8')
            if 'chassis=1 board=9' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 9 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2209')
                memlinecardPorts.append('9')
            if 'chassis=1 board=10' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 10 has route'.format(logNum,server,time.time()))
                linecardSlotsPopulated.append('2210')
                memlinecardPorts.append('10')
            if 'chassis=1 board=11' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 11 has route'.format(logNum,server,time.time()))
                podSlotsPopulated.append('2211')
                mempodPorts.append('11')
            if 'chassis=1 board=12' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 12 has route'.format(logNum,server,time.time()))
                podSlotsPopulated.append('2212')
                mempodPorts.append('12')
            if 'chassis=1 board=13' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 13 has route'.format(logNum,server,time.time()))
                podSlotsPopulated.append('2213')
                mempodPorts.append('13')
            if 'chassis=1 board=14' in line:
                print ('{:4d}\t{:15s}\t{:16.5f}\tMMI\tSlot 14 has route'.format(logNum,server,time.time()))
                podSlotsPopulated.append('2214')
                mempodPorts.append('14')
        if wait is not None:
            time.sleep(wait)

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        logger.logError(logNum, server, message)
        errorLog ('{:4d}\t{:15s}\t{:16.5f}\t{}'.format(logNum,server,time.time(),command))
        logger.logError(logNum, server,errorLog)
def memTest(logNum,server,session,command):
    try:
        if command is None:return
        session.sendline(command)
        session.prompt()
        lines = session.before.decode()
        for line in lines.splitlines():
            print ('{:4d}\t{:15s}\t{:16.5f}\t{}'.format(logNum,server,time.time(),line))
            if 'ERROR' in line:
                logMessage = 'MemTest Failed {} {}'.format(line,command)
                logger.logError(logNum,server,logMessage)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        logger.logError(logNum, server, message)
        print('Command Failed {:4d}\t{:15s}\t{:16.5f}\t{}'.format(logNum,server,time.time(),command))

