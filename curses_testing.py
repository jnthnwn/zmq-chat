import curses
from curses import wrapper


def main(stdscr):
    # create a colour pairing to reference later with '1'
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # hide the cursor from being displayed
    curses.curs_set(0)
    # set up a window that takes up the bottom half of the screen
    editwin = curses.newwin(curses.LINES//2, curses.COLS, curses.LINES//2, 0)

    # keep doing this for three key strokes
    for i in range(3):
        # start with a blank screen
        stdscr.clear()
        # print the counter to the screen
        stdscr.addstr(str(i))
        # update the screen contents
        stdscr.refresh()

        # associate the colour pair above with the 'bottom half' window
        editwin.bkgd(' ', curses.color_pair(1))
        # draw a box in it using the nice default chars
        editwin.box(0, 0)
        # editwin.addstr(0, 0, str(dir(editwin)), curses.color_pair(1))
        editwin.refresh()

        # wait for user to press key
        stdscr.getkey()

'''
Puts a wrapper around a callable that will create a window object,
turn off key-to-screen echoing, make applications react to keys instantly i.e. without waiting for a
return key signal, and handle special keys more nicely.
'''
wrapper(main)
