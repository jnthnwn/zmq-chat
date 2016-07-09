# ZMQ Chat
This is a simple chat client/server implementation to explore the base ZeroMQ
API and, later, try integrating some of the higher level patterns from the
[zguide](http://zguide.zeromq.org/).

### Interested in playing around with it?
At the moment, you'll have to start all three components in separate windows.
There are plans to incorporate curses and have a nice text-based interface
for the client text input and display. In the meantime...

Get the server running with:
```
git clone https://github.com/jnthnwn/zmq-chat.git
cd zmq-chat
pip install -r requirements.txt
python3 server.py 8888 8889
```

Get the client running with:
```
python3 client.py localhost 8888 testuser
```

Get the display running with:
```
python3 display.py localhost 8889
```

And you'll be able to do this:
![Chat client screenshot](/images/zmq_chat_screenshot.png)
