import zmq


def main():
  ctx = zmq.Context()
  client_sock = ctx.socket(zmq.REP)
  client_sock.bind('tcp://*:8888')
  
  while True:
    parts = client_sock.recv_multipart()
    print('received msg: {}'.format(str(parts)))
    client_sock.send_multipart(parts)
    print('sent reply: {}'.format(parts))


if '__main__' == __name__:
  main()
