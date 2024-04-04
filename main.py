import curses

from gui import GUI

def main(stdscr):
    GUI(stdscr).run()
    print("Thanks for using the XOR-Cipher App; See you next time!")

if __name__ == "__main__":
    curses.wrapper(main)
