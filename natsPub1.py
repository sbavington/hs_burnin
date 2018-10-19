#!/usr/bin/python3
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import natsPub
nc = NATS()

servers = ['nats://10.0.2.166:4222']
subject = 'burnin'
message = 'Burnin text'
def publish_log(message, loop):
	opts = {'servers': servers,'io_loop':loop}
	try:
		yield from nc.connect(**opts)
	except ErrNoServers as e:
		print (e)
		return
	if nc.is_connected:
		try:
			yield from nc.publish(subject, message.encode())
			yield from nc.flush(0.500)
		except ErrConnectionClosed as e:
			print ('Connection Closed')
		except ErrTimeout as e:
			print("Timeout occured when publishing msg i={}: {}".format(i, e))

		yield from nc.close()	
loop = asyncio.get_event_loop()
loop.run_until_complete(publish_log(message, loop))
loop.close()
