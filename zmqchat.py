import argparse
import configparser
import curses
import threading
import time
import zmq

from client import ClientChat
from curses import wrapper
from display import ClientDisplay

def parse_args():
    parser = argparse.ArgumentParser(description='Run a chat client')

    # maybe make selection of username interactive
    parser.add_argument('username',
                        type=str,
                        help='your preferred username')
    parser.add_argument('--config-file',
                        type=str,
                        help='path to an alternate config file, defaults to zmq-chat.cfg')

    return parser.parse_args()

def start_top_window(window, display):
    window_lines, window_cols = window.getmaxyx()
    bottom_line = window_lines - 1
    window.bkgd(curses.A_NORMAL, curses.color_pair(2))
    window.scrollok(1)
    while True:
        # alternate color pair used to visually check how frequently this loop runs
        # to tell when user input is blocking
        window.addstr(bottom_line, 1, display.recv_string())
        window.move(bottom_line, 1)
        window.scroll(1)
        window.refresh()

def start_bottom_window(window, chat_sender):
    window.bkgd(curses.A_NORMAL, curses.color_pair(2))
    window.clear()
    window.box()
    window.refresh()
    while True:
        window.clear()
        window.box()
        window.refresh()
        s = window.getstr(1, 1).decode('utf-8')
        if s is not None and s != "":
            chat_sender.send_string(s)
        # need to do sleep here...
        # if bottom window gets down to `window.getstr...` while top window is setting up,
        # it registers a bunch of control characters as the user's input
        time.sleep(0.005)

def main(stdscr):
    config_file = args.config_file if args.config_file is not None else 'zmq-chat.cfg'
    config = configparser.ConfigParser()
    config.read(config_file)
    config = config['default']

    receiver = zmq.Context().instance().socket(zmq.PAIR)
    receiver.bind("inproc://clientchat")
    sender = zmq.Context().instance().socket(zmq.PAIR)
    sender.connect("inproc://clientchat")
    client = ClientChat(args.username, config['server_host'],
                        config['chat_port'], receiver)
    client.run()

    display_receiver = zmq.Context().instance().socket(zmq.PAIR)
    display_receiver.bind("inproc://clientdisplay")
    display_sender = zmq.Context().instance().socket(zmq.PAIR)
    display_sender.connect("inproc://clientdisplay")
    display = ClientDisplay(config['server_host'], config['display_port'], display_sender)
    display.run()

    ### curses set up
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # ensure that user input is echoed to the screen
    curses.echo()
    curses.curs_set(0)

    window_height = curses.LINES
    window_width = curses.COLS
    division_line =  int(window_height * 0.8)

    # instaniate two pads - one for displaying received messages
    # and one for showing the message the user is about to send off
    top_pad = stdscr.subpad(division_line, window_width, 0, 0)
    bottom_pad = stdscr.subpad(window_height - division_line, window_width, division_line, 0)
    
    top_thread = threading.Thread(target=start_top_window, args=(top_pad, display_receiver))
    top_thread.daemon = True
    top_thread.start()

    bottom_thread = threading.Thread(target=start_bottom_window, args=(bottom_pad, sender))
    bottom_thread.daemon = True
    bottom_thread.start()

    top_thread.join()
    bottom_thread.join()


if '__main__' == __name__:
    try:
        args = parse_args()
        wrapper(main)
    except KeyboardInterrupt as e:
        pass
    except:
        raise
