#!/usr/bin/python

###
#	Python WebSocket Server for Raspberry Pi
#	PiFace web control
#	by David Art <david.madbox@gmail.com>
###

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import datetime
import json

import piface.pfio as pfio
pfio.init()

last_data = None

class WSHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		self.connected = True
		print 'new connection'
		self.timeout_loop()
	  
	def on_message(self, message):
		global last_data
		# print '> %s' % message
		pin = int(message)
		state = int(last_data['out'][pin])
		# invert (toggle)
		state = not bool(state)
		pfio.digital_write(pin, state)
 
	def on_close(self):
		self.connected = False
		print 'connection closed'
	  
	def timeout_loop(self):
		# read PiFace input/output state
		global last_data
		r_input = '{0:08b}'.format(pfio.read_input())
		r_output = '{0:08b}'.format(pfio.read_output())

		data = {"in": [], "out": []}

		for i in range(8):
			data['in'].append(r_input[7-i])
			data['out'].append(r_output[7-i])

		if data != last_data:
			self.write_message(json.dumps(data))
		last_data = data

		# here come the magic part .. loop
		if self.connected:
			tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=.5), self.timeout_loop)
 
 
application = tornado.web.Application([
	(r'/piface', WSHandler),
])

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	print 'Raspberry Pi - PiFace'
	print 'WebSocket Server start ..'
	tornado.ioloop.IOLoop.instance().start()

