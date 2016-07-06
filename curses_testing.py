import curses
from curses import wrapper


def main(stdscr):
    # create a colour pairing to reference later with '1'
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # hide the cursor from being displayed
    # curses.curs_set(0)
    curses.echo()

    # set up a window that takes up the top half of the screen
    # and a window that takes up the bottom half
    topwin = curses.newwin(curses.LINES-3, curses.COLS, 0, 0)
    bottomwin = curses.newwin(3, curses.COLS, curses.LINES-3, 0)

    # update the screen contents
    stdscr.refresh()

    # associate the colour pair above with the 'top half' window
    topwin.bkgd(' ', curses.color_pair(1))
    # draw a box in it using the nice default chars
    topwin.box(0, 0)
    topwin.refresh()

    # do similarly for the bottom window
    bottomwin.bkgd(' ', curses.color_pair(1))
    while True:
        bottomwin.clear()
        bottomwin.box(0, 0)
        bottomwin.move(1, 1)
        s = bottomwin.getstr()
        topwin.clear()
        topwin.addstr(1, 1, s)
        topwin.box(0, 0)
        topwin.refresh()
        bottomwin.refresh()

    # wait for user to press key
    stdscr.getkey()

'''
Puts a wrapper around a callable that will create a window object,
turn off key-to-screen echoing, make applications react to keys instantly i.e. without waiting for a
return key signal, and handle special keys more nicely.
'''
wrapper(main)
