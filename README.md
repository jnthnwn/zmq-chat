# ZMQ Chat
This is a simple chat client/server implementation to explore the base ZeroMQ
API and, later, try integrating some of the higher level patterns from the
[zguide](http://zguide.zeromq.org/).

### Try it out!
At the moment, you'll have to start all three components in separate windows.
There are plans to incorporate the `curses` library and have a nice text-based interface
for the client text input and display. In the meantime...

Get the server running with:
```
git clone https://github.com/jnthnwn/zmq-chat.git
cd zmq-chat
pip install -r requirements.txt
python3 server.py
```

Get the client running with:
```
python3 client.py <username>
```

Get the display running with:
```
python3 display.py
```

You can modify the configuration file `zmq-chat.cfg` as you wish,
but the defaults will suffice for just playing around.

Now you'll be able to do this:
![Chat client screenshot](/images/zmq_chat_screenshot.png)
