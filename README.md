# ZMQ Chat 👏 👏 👏 
This is a simple chat client/server implementation to explore the base ZeroMQ
API and, later, try integrating some of the higher level patterns from the
[zguide](http://zguide.zeromq.org/). Also utilizes the 
[curses](https://docs.python.org/3/howto/curses.html) library to provide
a text-based user interface.

The client uses a mix of multithreading and ZeroMQ's asynchronous I/O model
to separately update the message display/text input interfaces, communicate
between components, and send messages and receive replies from the server.

The server simply exposes a port for incoming messages and broadcasts them
to all currently connected clients.

If you somehow come across this project and can provide some feedback or ways
to improve it, please do!

### Try it out!

Install the project (requires Python3 and pip):
```
git clone https://github.com/jnthnwn/zmq-chat.git
cd zmq-chat
pip3 install -r requirements.txt
```

Get the server running:
```
python3 server.py
```

Get your clients connected:
```
python3 zmqchat.py <username>
```

You can modify the configuration file `zmq-chat.cfg` to specify
a particular server host or ports to use,
but the defaults will suffice for just playing around.

Now you'll be able to do this:

![gif of chat clients talking](/images/asciicast.gif)
