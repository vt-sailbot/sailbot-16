#!/usr/bin/python

import socket
import sys
from thread import *
import time
import json
import threading
from gps import *

gpsd = None  # global GPSD variable
gpsd_data = {}

# define the socket parameters
HOST = ''
PORT = 8907

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# bind socket to local host and port
try:
    connection.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' \
        + msg[1]
    sys.exit()

print 'Socket bind complete'

# GPSD polling class definitions
class GPSPoller(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd  # bring it in scope
        gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info
        self.current_value = None
        self.running = True  # setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()  # this will continue to loop and grab each set of gpsd info to clear the buffer

# create and start the GPSD thread
gpsp = GPSPoller()
gpsp.start()

# Start listening on socket
connection.listen(10)
print 'Socket now listening'

# function for handling connections; will be used to create threads
def clientthread(conn):

    # infinite loop so that function do not terminate and thread do not end
    while True:

        # updates the data dictionary        
        update_gpsd_data()

        # receive data from the client
        data = conn.recv(1024)
        if not data:
            break
        print 'Received %s from the server.' % data

        if data == '0':
            print 'Sending: %s' % json.dumps(gpsd_data).encode('utf-8')
            conn.sendall(json.dumps(gpsd_data).encode('utf-8'))

    # close the connection if the client if the client and server connection is interfered
    conn.close()

def update_gpsd_data():
    print 'Updating GPS data!'
    try:
        # tries to pull in all the critical GPS data
        gpsd_data.clear()
        gpsd_data.update({
            'latitude': gpsd.fix.latitude,
            'longitude': gpsd.fix.latitude,
            'timestamp': gpsd.fix.time,
            'heading': gpsd.attitude.heading,
            'speed': gpsd.fix.speed,
            'roll': gpsd.attitude.roll,
            'pitch': gpsd.attitude.pitch,
            'yaw': gpsd.attitude.yaw,
            })
    except AttributeError:
        # Uses standard GPS data for units that have unsupported features
        gpsd_data.update({
            'latitude': gpsd.fix.latitude,
            'longitude': gpsd.fix.latitude,
            'timestamp': gpsd.fix.time,
            'speed': gpsd.fix.speed,
            })
    
    print gpsd_data

# main loop to keep the server process going
while True:

    # wait to accept a connection in a blocking call
    (conn, addr) = connection.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function

    start_new_thread(clientthread, (conn, ))

connection.close()

            