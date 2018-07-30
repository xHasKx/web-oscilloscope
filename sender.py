#!/usr/bin/env python3
import socket
import random
from array import array

# create random array
points = array('H')
for i in range(625):
	points.append(random.randint(0, 65535))

UDP_IP = "127.0.0.1"
UDP_PORT = 1234
MESSAGE = points.tobytes()

'''
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)
'''

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
