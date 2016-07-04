import argparse
import zmq


class ZMQChatServer(object):

    def __init__(self, chat_interface, chat_port, display_interface, display_port):
        self.chat_interface = chat_interface
        self.chat_port = chat_port
        self.display_interface = display_interface
        self.display_port = display_port
        self.context = zmq.Context()
        self.chat_sock = None
        self.display_sock = None

    def bind_ports(self):
        self.chat_sock = self.context.socket(zmq.REP)
        chat_bind_string = 'tcp://{}:{}'.format(
            self.chat_interface, self.chat_port)
        self.chat_sock.bind(chat_bind_string)

        self.display_sock = self.context.socket(zmq.PUB)
        display_bind_string = 'tcp://{}:{}'.format(
            self.display_interface, self.display_port)
        self.display_sock.bind(display_bind_string)

    def get_message_with_identity(self):
        parts = self.chat_sock.recv_multipart()
        print(parts)
        identity, message = [s.decode() for s in parts]
        return [identity, message]

    def update_displays(self, identity, message):
        parts = [identity, message]
        parts = [bytes(s, 'utf-8') for s in parts]
        self.chat_sock.send(b'\x00')
        self.display_sock.send_multipart(parts)

    def start_main_loop(self):
        self.bind_ports()
        while True:
            identity, message = self.get_message_with_identity()
            self.update_displays(identity, message)


def parse_args():
    parser = argparse.ArgumentParser(description='Run the chat server')

    parser.add_argument('chat_port',
                        type=str,
                        help='port to expose for chat messages')
    parser.add_argument('display_port',
                        type=str,
                        help='port to expose for display messages')

    return parser.parse_args()


if '__main__' == __name__:
    args = parse_args()
    server = ZMQChatServer('*', args.chat_port, '*', args.display_port)
    server.start_main_loop()
