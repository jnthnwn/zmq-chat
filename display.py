import sys
import zmq


def main():
  args = parse_args()
  
  hostname = args.hostname
  port = args.port
  ctx = zmq.Context()
  chatroom_sock = ctx.socket(zmq.SUB)
  chatroom_sock.setsockopt_string(zmq.SUBSCRIBE, '')
  chatroom_sock.connect('tcp://{}:{}'.format(hostname, port))
  while True:
    reply = chatroom_sock.recv_multipart()
    user, msg = [s.decode() for s in reply]
    print('{}: {}'.format(user, msg))


def parse_args():
  parser = argparse.ArgumentParser(description='Run the chat display')
  parser.add_argument('hostname',
          type=str,
          help='hostname of the chat server')
  parser.add_argument('port',
          type=str,
          help='port used for the chat server display')


if '__main__' == __name__:
  main()
