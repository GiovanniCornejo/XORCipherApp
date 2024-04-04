import curses

from gui import GUI

def main(stdscr):
    GUI(stdscr).run()

if __name__ == "__main__":
    curses.wrapper(main)
    print("Thanks for using the XOR-Cipher App; See you next time!")
