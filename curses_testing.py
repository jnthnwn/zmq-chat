import curses
from curses import wrapper


def main(stdscr):
    for i in range(10):
        # start with a blank screen
        stdscr.clear()
        # print the counter to the screen
        stdscr.addstr(str(i))
        # update the screen contents
        stdscr.refresh()
        # wait for user to press key
        stdscr.getkey()

'''
Puts a wrapper around a callable that will create a window object,
turn off key-to-screen echoing, make applications react to keys instantly i.e. without waiting for a
return key signal, and handle special keys more nicely.
'''
wrapper(main)
