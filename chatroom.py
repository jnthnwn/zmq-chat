import zmq


def main():
  ctx = zmq.Context()
  client_sock = ctx.socket(zmq.REP)
  client_sock.bind('tcp://*:8888')
  display_sock = ctx.socket(zmq.PUB)
  display_sock.bind('tcp://*:8889')
  
  while True:
    parts = client_sock.recv_multipart()
    identity, msg = [s.decode() for s in parts]
    client_sock.send(b'\x00')
    display_sock.send_multipart(parts)


if '__main__' == __name__:
  main()
