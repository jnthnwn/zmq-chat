import argparse
import sys
import threading
import zmq


class ZMQChatClient(object):

    def __init__(self, username, server_host, server_port, chat_pipe):
        self.username = username
        self.server_host = server_host
        self.server_port = server_port
        self.context = zmq.Context()
        self.chat_sock = None
        self.chat_pipe = chat_pipe
        self.poller = zmq.Poller()

    def connect_to_server(self):
        self.chat_sock = self.context.socket(zmq.REQ)
        connect_string = 'tcp://{}:{}'.format(
            self.server_host, self.server_port)
        self.chat_sock.connect(connect_string)

    def reconnect_to_server(self):
        self.chat_sock.setsockopt(zmq.LINGER, 0)
        self.chat_sock.close()
        self.poller.unregister(self.chat_sock)
        self.connect_to_server()

    def register_with_poller(self):
        self.poller.register(self.chat_sock, zmq.POLLIN)

    def prompt_for_message(self):
        return self.chat_pipe.recv_string()

    def send_message(self, msg):
        parts = [self.username, msg]
        self.chat_sock.send_multipart([bytes(part, 'utf-8') for part in parts])

    def get_reply(self):
        return self.chat_sock.recv()

    def has_message(self):
        events = dict(self.poller.poll(1000))
        return events.get(self.chat_sock) == zmq.POLLIN

    def start_main_loop(self):
        self.connect_to_server()
        self.register_with_poller()

        while True:
            msg = self.prompt_for_message()
            self.send_message(msg)
            if self.has_message():
                reply = self.get_reply()
            else:
                self.reconnect_to_server()

    def run(self):
        thread = threading.Thread(target=self.start_main_loop)
        thread.start()


def parse_args():
    parser = argparse.ArgumentParser(description='Run a chat client')

    parser.add_argument('hostname',
                        type=str,
                        help='hostname of the chat server')
    parser.add_argument('port',
                        type=str,
                        help='port used for the chat server')
    # maybe make selection of username interactive
    parser.add_argument('username',
                        type=str,
                        help='your preferred username')

    return parser.parse_args()


if '__main__' == __name__:
    args = parse_args()
    receiver = zmq.Context().instance().socket(zmq.PAIR)
    receiver.bind("inproc://clientchat")
    sender = zmq.Context().instance().socket(zmq.PAIR)
    sender.connect("inproc://clientchat")
    client = ZMQChatClient(args.username, args.hostname, args.port, receiver)
    # client.start_main_loop()
    client.run()


    while True:
        s = input('> ')
        sender.send_string(s)
