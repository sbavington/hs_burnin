#!/usr/bin/python3

import sys
import usb.core
# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
	#if '1027' in str(cfg.idVendor): 
	print ('Vendor:{} Address:{} bus:{}'.format(str(cfg.idVendor),str(cfg.address),str(cfg.bus)))
	print (cfg)
