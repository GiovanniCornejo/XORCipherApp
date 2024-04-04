import curses

class GUI:
    # Container for application
    OVERLAY_ROWS, OVERLAY_COLS = 24, 80
    # Display menu below top of overlay 
    MENU_ROWS, MENU_COLS = 10, 40
    MENU_Y, MENU_X = 2, 20
    # Display output of text, key below menu
    OUTPUT_ROWS, OUTPUT_COLS = 4, 76
    OUTPUT_Y, OUTPUT_X = MENU_ROWS + MENU_Y, 2
    # Display prompt below text, key
    PROMPT_ROWS, PROMPT_COLS = 6, 78
    PROMPT_Y, PROMPT_X = OUTPUT_ROWS + OUTPUT_Y + 1, 1
    # Display user input below prompt
    INPUT_ROWS, INPUT_COLS = 3, 68
    INPUT_Y, INPUT_X = PROMPT_Y + 2, 6
    """
    Start on 18th row, 2nd column and be 6 x 78 
2) Display prompt, centered, on 2nd row 
3) Display box, centered, under prompt, size 3x68 
4) Allow entry of 65 characters on one line only 
"""

    # ----------------------------------- Init ----------------------------------- #

    def __init__(self, stdscr: curses.window):
        curses.curs_set(0) # No cursor
        curses.noecho() # Type without it showing
        curses.cbreak() # React to keys instantly

        # Default Text and Key values
        self.key = "But there's one sound that no one knows... What does the Fox say?".encode('cp437')
        self.text = "This is a haiku; it is not too long I think; but you may disagree".encode('cp437')

        self.button = "startup"

        # Initialize Menus
        self.background = stdscr
        self.status = "Application started successfully."
        self.background.addstr(self.OVERLAY_ROWS, 0, self.status)

        self.overlay = self.init_overlay()
        self.menu = self.init_menu()
        self.output = self.init_output()
        self.prompt = self.init_prompt()
        self.input = self.init_input()

        # Initial Display
        self.update_status()
        self.update_text_and_key()

        self.background.refresh()
        self.overlay.refresh()
        self.menu.refresh()
        self.output.refresh()

    def init_overlay(self):
        """Initialize the overlay window."""
        window = curses.newwin(self.OVERLAY_ROWS, self.OVERLAY_COLS, 0, 0)
        window.box()

        message = "Welcome to the XOR-Cipher App!"
        x = self.OVERLAY_COLS // 2 - len(message) // 2 # Center text
        window.addstr(1, x, message)

        return window
    
    def init_menu(self):
        """Initialize the menu window contained within the overlay window."""
        window = curses.newwin(self.MENU_ROWS, self.MENU_COLS, self.MENU_Y, self.MENU_X)
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
    
    def init_output(self):
        """Initialize the display window contained within the overlay window."""
        window = curses.newwin(self.OUTPUT_ROWS, self.OUTPUT_COLS, 
                               self.OUTPUT_Y, self.OUTPUT_X)
        window.box()
        return window
    
    def init_prompt(self):
        """Initialize the prompt window contained within the overlay window."""
        window = curses.newwin(self.PROMPT_ROWS, self.PROMPT_COLS, self.PROMPT_Y, self.PROMPT_X)
        window.box()
        return window
    
    def init_input(self):
        """Initialize the user input window contained within the prompt window"""
        window = curses.newwin(self.INPUT_ROWS, self.INPUT_COLS, self.INPUT_Y, self.INPUT_X)
        window.box()
        return window
    

    # ------------------------------ Run Application ----------------------------- #
    
    def run(self):
        """
        Runs the program with the provided background object.
        """
        while self.button != 'Q':
            # Cipher Commands
            if self.button == 'startup':
                pass
            # Input Commands
            else:
                self.run_prompt()

            self.button = self.background.getkey().upper()

    def run_prompt(self):
        """
        Handle the current input command or benchmarking

        Parameters:
        message: The message to prompt to the user.        
        """

        # Get Current Prompt
        if self.button == 'F':
            message = "Enter file to load, then press [ENTER]"

        x = self.PROMPT_COLS // 2 - len(message) // 2 # Center text
        self.prompt.addstr(1, 1, " " * (self.PROMPT_COLS - 3))
        self.prompt.addstr(1, x, message)
        self.prompt.refresh()

        # TODO: Implement each input command
        # TODO: Implement special display for benchmarking

        self.input.refresh()
    
    # ------------------------------ Input Commands ------------------------------ #

    def read_from_file(self):
        """Read text from a local file."""
        pass

    def read_from_input(self):
        """Read text from user input prompt."""
        pass

    def change_cipher_key(self):
        """Change key used for ciphers."""
        pass

    # ------------------------------ Cipher Commands ----------------------------- #

    def apply_rust_cipher(self):
        """Apply Rust cipher to text."""
        pass

    def apply_python_cipher(self):
        """Apply Python cipher to text"""
        pass

    def verify_cipher_results(self):
        """Verify cipher results."""
        pass

    def run_benchmarks(self):
        """Run benchmarks on text for Rust and Python cipher."""
        pass

    # ------------------------------ Update Display ------------------------------ #

    def update_text_and_key(self):
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

        self.output.addstr(1, 2," " * (self.OUTPUT_COLS - 3))
        self.output.addstr(1, 2, "TEXT [" + str_text + "]")

        self.output.addstr(2, 2," " * (self.OUTPUT_COLS - 3))
        self.output.addstr(2, 2, "KEY  [" + str_key + "]")
            
    def update_status(self):
        """Update the status shown."""
        self.background.addstr(self.OVERLAY_ROWS, 0, " " * self.OUTPUT_COLS)
        self.background.addstr(self.OVERLAY_ROWS, 0, "Status: " + self.status)
