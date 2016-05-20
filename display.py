import zmq
import sys


def main():
  ctx = zmq.Context()
  chatroom_sock = ctx.socket(zmq.SUB)
  chatroom_sock.setsockopt_string(zmq.SUBSCRIBE, '')
  chatroom_sock.connect('tcp://localhost:8889')
  while True:
    reply = chatroom_sock.recv_multipart()
    user, msg = [s.decode() for s in reply]
    print('{}: {}'.format(user, msg))


if '__main__' == __name__:
  main()
