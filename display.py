import argparse
import configparser
import sys
import threading
import zmq


class ClientDisplay(object):

    def __init__(self, server_host, server_port, display_pipe):
        self.server_host = server_host
        self.server_port = server_port
        self.context = zmq.Context()
        self.display_sock = None
        self.display_pipe = display_pipe
        self.poller = zmq.Poller()

    def connect_to_server(self):
        self.display_sock = self.context.socket(zmq.SUB)
        self.display_sock.setsockopt_string(zmq.SUBSCRIBE, '')
        connect_string = 'tcp://{}:{}'.format(
            self.server_host, self.server_port)
        self.display_sock.connect(connect_string)
        self.poller.register(self.display_sock, zmq.POLLIN)

    def get_update(self):
        data = self.display_sock.recv_json()
        username, message = data['username'], data['message']
        self.display_pipe.send_string('{}: {}'.format(username, message))

    def has_message(self):
        events = self.poller.poll()
        return self.display_sock in events

    def start_main_loop(self):
        self.connect_to_server()
        while True:
            self.get_update()

    def run(self):
        thread = threading.Thread(target=self.start_main_loop)
        thread.daemon = True
        thread.start()
