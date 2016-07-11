import sys
import threading
import zmq


class ClientChat(object):

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
        self.poller.unregister(self.chat_sock)
        self.chat_sock.setsockopt(zmq.LINGER, 0)
        self.chat_sock.close()
        self.connect_to_server()
        self.register_with_poller()

    def register_with_poller(self):
        self.poller.register(self.chat_sock, zmq.POLLIN)

    def prompt_for_message(self):
        return self.chat_pipe.recv_string()

    def send_message(self, message):
        data = {
            'username': self.username,
            'message': message,
        }
        self.chat_sock.send_json(data)

    def get_reply(self):
        self.chat_sock.recv()

    def has_message(self):
        events = dict(self.poller.poll(3000))
        return events.get(self.chat_sock) == zmq.POLLIN

    def start_main_loop(self):
        self.connect_to_server()
        self.register_with_poller()

        while True:
            message = self.prompt_for_message()
            self.send_message(message)
            if self.has_message():
                self.get_reply()
            else:
                self.reconnect_to_server()

    def run(self):
        thread = threading.Thread(target=self.start_main_loop)
        # make sure this background thread is daemonized
        # so that when user sends interrupt, whole program stops
        thread.daemon = True
        thread.start()
