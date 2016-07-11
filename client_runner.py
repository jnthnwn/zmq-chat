import argparse
import configparser
import zmq

from client import ClientChat

def parse_args():
    parser = argparse.ArgumentParser(description='Run a chat client')

    # maybe make selection of username interactive
    parser.add_argument('username',
                        type=str,
                        help='your preferred username')
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

        receiver = zmq.Context().instance().socket(zmq.PAIR)
        receiver.bind("inproc://clientchat")
        sender = zmq.Context().instance().socket(zmq.PAIR)
        sender.connect("inproc://clientchat")
        client = ClientChat(args.username, config['server_host'],
                            config['chat_port'], receiver)
        client.run()

        while True:
            s = input('> ')
            sender.send_string(s)

    except KeyboardInterrupt:
        pass
