import zmq
import sys


def main():
  identity = sys.argv[1]
  ctx = zmq.Context()
  chatroom_sock = ctx.socket(zmq.REQ)
  chatroom_sock.connect('tcp://localhost:8888')
  while True:
    msg = input('> ')
    parts = [identity, msg]
    parts = [bytes(part, 'utf-8') for part in parts]
    chatroom_sock.send_multipart(parts)
    print('sent msg: {}'.format(parts))
    reply = chatroom_sock.recv()
    print('received reply: {}'.format(str(reply)))


if '__main__' == __name__:
  main()
