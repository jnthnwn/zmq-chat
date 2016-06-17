import argparse
import sys
import zmq


def main():
  args = parse_args()

  identity = args.username
  hostname = args.hostname
  port = args.port
  ctx = zmq.Context()
  chatroom_sock = ctx.socket(zmq.REQ)
  chatroom_sock.connect('tcp://{}:{}'.format(hostname, port)
  poller = zmq.Poller()
  poller.register(chatroom_sock, zmq.POLLIN)

  while True:
    msg = input('> ')
    parts = [identity, msg]
    chatroom_sock.send_multipart([bytes(part, 'utf-8') for part in parts])

    # wait up to 1000 ms for a reply
    events = dict(poller.poll(1000))
    if events.get(chatroom_sock) == zmq.POLLIN:
      reply = chatroom_sock.recv()
    else:
      print('failed to send message - response timed out')
      chatroom_sock.setsockopt(zmq.LINGER, 0)
      chatroom_sock.close()
      poller.unregister(chatroom_sock)
      chatroom_sock = ctx.socket(zmq.REQ)
      chatroom_sock.connect('tcp://{}:{}'.format(hostname, port))
      poller.register(chatroom_sock, zmq.POLLIN)


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


if '__main__' == __name__:
  main()
