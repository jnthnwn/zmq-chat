import zmq
import sys


def main():
  identity = sys.argv[1]
  ctx = zmq.Context()
  chatroom_sock = ctx.socket(zmq.REQ)
  chatroom_sock.connect('tcp://localhost:8888')
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
      chatroom_sock.connect('tcp://localhost:8888')
      poller.register(chatroom_sock, zmq.POLLIN)


if '__main__' == __name__:
  main()
