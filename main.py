import curses

from tui import TUI

def main(stdscr):
    TUI(stdscr).run()

if __name__ == "__main__":
    curses.wrapper(main)
    print("Thanks for using the XOR-Cipher App; See you next time!")
