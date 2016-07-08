import argparse
import sys
import zmq


class ClientDisplay(object):

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.context = zmq.Context()
        self.display_sock = None

    def connect_to_server(self):
        self.display_sock = self.context.socket(zmq.SUB)
        self.display_sock.setsockopt_string(zmq.SUBSCRIBE, '')
        connect_string = 'tcp://{}:{}'.format(
            self.server_host, self.server_port)
        self.display_sock.connect(connect_string)

    def get_update(self):
        data = self.display_sock.recv_json()
        username, message = data['username'], data['message']
        print('{}: {}'.format(username, message))

    def start_main_loop(self):
        self.connect_to_server()
        while True:
            self.get_update()


def parse_args():
    parser = argparse.ArgumentParser(description='Run the chat display')

    parser.add_argument('hostname',
                        type=str,
                        help='hostname of the chat server')
    parser.add_argument('port',
                        type=str,
                        help='port used for the chat server display')

    return parser.parse_args()


if '__main__' == __name__:
    args = parse_args()
    display = ClientDisplay(args.hostname, args.port)
    display.start_main_loop()
