#!/usr/bin/python3

import threading
import time
import datetime
from random import randint
import hs_comm as comm
from pexpect import pxssh
n = 100
threads = []
servers = ['10.0.2.195']

user = 'root'
passwd = 'root'

def cmm_login(server,logNum):
	CMM_session = pxssh.pxssh()
	podSlotsPopulated = []
	linecardSlotsPopulated = []
	memlinecardPorts = []
	mempodPorts = []
	port = 22
	comm.Login(logNum,
		CMM_session,
		server,
		port,
		user,
		passwd)
	commands = [{'command' : './hs_eeprom readAll' , 'wait' : 2},
		{'command' : 'hs_bis_info.py' , 'wait' : 2},
		{'command' : 'SysManComm on' , 'wait' : 120},
		{'command' : 'mmi_route' , 'wait' : 5},
		{'command' : 'mmi_stats' , 'wait' : 2}]
	for command in commands:
		comm.sessionCommand(logNum,
		server,
		CMM_session,
		command.get('command'),
		command.get('wait'),
		podSlotsPopulated,
		linecardSlotsPopulated,
		memlinecardPorts,
		mempodPorts)
	for linecard in memlinecardPorts:
		print ('{:4d}\t{:15s}\t{:16.5f}\tFor linecard port {}'.format(logNum,server,time.time(),linecard))
		for targetLinecard in memlinecardPorts:
			print ('{:4d}\t{:15s}\t{:16.5f}\tMemory test from port {} to port {}'.format(logNum,server,time.time(),linecard,targetLinecard))
			command = "hs_mem_test --dma_addr=1:{}:0 --gen_addr=1:2:0 --val_addr=1:2:0 --max_in_flight=255 gen_val_test 0 536870912".format(targetLinecard)
			
			comm.memTest(logNum,server,CMM_session,command)
		for pod in mempodPorts:
			print ('{:4d}\t{:15s}\t{:16.5f}\tMemory test from port {} to port {}'.format(logNum,server,time.time(),linecard,pod))
			command = "hs_mem_test --dma_addr=1:{}:0 --gen_addr=1:2:0 --val_addr=1:2:0 --max_in_flight=255 gen_val_test 0 536870912".format(pod)
			comm.memTest(logNum,server,CMM_session,command)
	cmm_threads =[]
	for pod in podSlotsPopulated:
		t = threading.Thread(name = pod, 
			target = pod_thread,
			args = (pod,server,logNum))
	
		t.start()
		cmm_threads.append(t)
			
	for lcard in linecardSlotsPopulated:
		t = threading.Thread(name = lcard,
		target = line_card_thread, 
		args = (lcard,server,logNum))
		
		t.start()
		cmm_threads.append(t)
			
	for thread in cmm_threads:
		thread.join()
	commands = [{'command' : 'SysManComm off' , 'wait' : 2}]
	for command in commands:
		comm.sessionCommand(logNum,
		server,
		CMM_session,
		command.get('command'),
		command.get('wait'))
	print ('{:4d}\t{:15s}\t{:16.5f}\t All Tests Completed'.format(logNum,server,time.time()))

def line_card_thread(lcard,server,logNum):
	print ('{:4d}\t{:15s}\t{:16.5f}\t Going to lincard {}'.format(logNum,server,time.time(),lcard))
	linecard_session = pxssh.pxssh()
	comm.Login(logNum,
		linecard_session,
		server,
		lcard,
		user,
		passwd)
	time.sleep(5)
	commands = [{'command' : 'hs_bis_info.py', 'wait' : 2},
			{'command' : 'mmi_route', 'wait' : 2},
			{'command' : 'mmi_stats', 'wait' :2}]
	for command in commands:
		comm.sessionCommand(logNum,
		server,
		linecard_session,
		command.get('command'),
		command.get('wait'))
		
def pod_thread(pod,server,logNum):	
	print ('{:4d}\t{:15s}\t{:16.5f}\t Going to pod {}'.format(logNum,server,time.time(),pod))
	pod_session = pxssh.pxssh()
	comm.Login(logNum,
		pod_session,
		server,
		pod,
		user,
		passwd)
	time.sleep(5)
	commands = [{'command' : 'hs_bis_info.py', 'wait' : 2},
			{'command' : 'mmi_route', 'wait' : 2},
			{'command' : 'mmi_stats', 'wait' :2}]
	for command in commands:
		comm.sessionCommand(logNum,
		server,
		pod_session,
		command.get('command'),
		command.get('wait'))
for i in range(n):		
	for server in servers:
		logNum = (randint(1000,9999))
		t = threading.Thread(name = 'CMM_Login', target=cmm_login, args=(server,logNum))
		t.start()
		threads.append(t)
	for thread in threads:
		thread.join()
	time.sleep(10)	
print ('==================All Testing Completed ===========================================\n\n'.format(time.time()))
