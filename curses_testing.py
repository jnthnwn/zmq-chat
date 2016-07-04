import curses
from curses import wrapper


def main(stdscr):
    stdscr.clear()

    for i in range(10):
        stdscr.addstr(str(i))
        stdscr.refresh()
        stdscr.getkey()


wrapper(main)
