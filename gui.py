import curses

class GUI:
    def __init__(self, stdscr: curses.window):
        curses.curs_set(0) # No cursor
        curses.noecho() # Type without it showing
        curses.cbreak() # React to keys instantly

        self.background = stdscr
        self.overlay_window = self.init_overlay()

    def init_overlay(self):
        overlay_window = curses.newwin(24, 80, 0, 0)
        overlay_window.box()

        # Welcome Message
        _, w = overlay_window.getmaxyx()
        intro_message = "Welcome to the XOR-Cipher App!"
        x = w // 2 - len(intro_message) // 2 # Center text
        y = 1
        overlay_window.addstr(y, x, intro_message)

        return overlay_window
    
    def run(self):
        """
        Runs the program with the provided background object.
        """

        key = "But there's one sound that no one knows... What does the Fox say?".encode('cp437')
        text = "This is a haiku; it is not too long I think; but you may disagree".encode('cp437')

        button = "startup"
        while button.lower() != 'q':
            self.background.clear()

            self.background.refresh()
            self.overlay_window.refresh()
            button = self.background.getkey()