import zmq


def main():
  ctx = zmq.Context()
  client_sock = ctx.socket(zmq.REP)
  client_sock.bind('tcp://*:8888')
  
  while True:
    parts = client_sock.recv_multipart()
    identity, msg = [s.decode() for s in parts]
    print('{}: {}'.format(identity, msg))
    client_sock.send(b'\x00')


if '__main__' == __name__:
  main()
