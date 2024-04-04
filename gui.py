import curses

class GUI:
    def __init__(self, stdscr: curses.window):
        curses.curs_set(0) # No cursor
        curses.noecho() # Type without it showing
        curses.cbreak() # React to keys instantly

        # Default Text and Key values
        self.key = "But there's one sound that no one knows... What does the Fox say?".encode('cp437')
        self.text = "This is a haiku; it is not too long I think; but you may disagree".encode('cp437')

        # Initialize Menus
        self.background = stdscr
        self.overlay = self.init_overlay()
        self.menu = self.init_menu()
        self.display = self.init_display()

    def init_overlay(self):
        """Initialize the overlay window."""
        window = curses.newwin(24, 80, 0, 0)
        window.box()

        _, w = window.getmaxyx()
        intro_message = "Welcome to the XOR-Cipher App!"
        x = w // 2 - len(intro_message) // 2 # Center text
        y = 1
        window.addstr(y, x, intro_message)

        return window
    
    def init_menu(self):
        """Initialize the menu window contained within the overlay window."""
        _, w = self.overlay.getmaxyx()
        window = curses.newwin(10, 40, 2, w // 2 - 20)
        window.box()
    
        menu = [
            '[F] Read text from a local File', 
            '[I] Read text from user Input prompt', 
            '[R] Apply Rust cipher to this text', 
            '[P] Apply Python cipher to this text', 
            '[V] Verify cipher results match', 
            '[K] Change Key used for ciphers', 
            '[B] Run Benchmarks on text (100000x)', 
            '[Q] Quit the Application'
        ]

        for i, item in enumerate(menu):
            window.addstr(i + 1, 2, item)  # Add each item on a new line with padding
        
        return window
    
    def init_display(self):
        """Initialize the display window contained within the overlay window."""
        _, w = self.overlay.getmaxyx()
        window = curses.newwin(4, 76, 2 + 10, w // 2 - 38)
        window.box()
        return window
    
    def update_display(self):
        """Update the display window with the current text and key."""
        ctrl_translation = str.maketrans(
            bytes(range(0, 32)).decode("cp437"),
            "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼"
        )

        str_text = self.text.decode('utf-8').translate(ctrl_translation)
        str_key = self.key.decode('utf-8').translate(ctrl_translation)

        if len(str_text) > 65:
            str_text = str_text[0:65]
        
        if len(str_key) > 65:
            str_key = str_key[0:65]

        # Clear previous text and key
        self.display.move(1, 2)
        self.display.addstr(" " * (self.display.getmaxyx()[1] - 3))
        self.display.move(2, 2)
        self.display.addstr(" " * (self.display.getmaxyx()[1] - 3))

        self.display.addstr(1, 2, "TEXT [" + str_text + "]")
        self.display.addstr(2, 2, "KEY  [" + str_key + "]")
        self.display.refresh()

    def run(self):
        """
        Runs the program with the provided background object.
        """

        button = "startup"
        self.background.refresh()
        self.overlay.refresh()
        self.menu.refresh()
        while button.lower() != 'q':


            self.update_display()
            button = self.background.getkey()