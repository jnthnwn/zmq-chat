import argparse
import configparser
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

    parser.add_argument('--config-file',
                        type=str,
                        help='path to an alternate config file, defaults to zmq-chat.cfg')

    return parser.parse_args()


if '__main__' == __name__:
    try:
        args = parse_args()
        config_file = args.config_file if args.config_file is not None else 'zmq-chat.cfg'
        config = configparser.ConfigParser()
        config.read(config_file)
        config = config['default']

        display = ClientDisplay(config['server_host'], config['display_port'])
        display.start_main_loop()

    except KeyboardInterrupt:
        pass
