import curses
from curses.textpad import Textbox, rectangle

class TUI:
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
        self.overlay = self.init_overlay()
        self.menu = self.init_menu()
        self.output = self.init_output()
        self.prompt = self.init_prompt()
        self.input, self.textwin = self.init_input()

        # Initial Display
        self.update_status("Application started successfully.")
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
        window = curses.newwin(self.OUTPUT_ROWS, self.OUTPUT_COLS, self.OUTPUT_Y, self.OUTPUT_X)
        window.box()
        return window
    
    def init_prompt(self):
        """Initialize the prompt window contained within the overlay window."""
        window = curses.newwin(self.PROMPT_ROWS, self.PROMPT_COLS, self.PROMPT_Y, self.PROMPT_X)
        return window
    
    def init_input(self):
        """Initialize the user input window contained within the prompt window"""
        window = curses.newwin(self.INPUT_ROWS, self.INPUT_COLS, self.INPUT_Y, self.INPUT_X)
        text_win = curses.newwin(1, self.INPUT_COLS - 2, self.INPUT_Y + 1, self.INPUT_X + 1)
        return window, text_win
    

    # ------------------------------ Run Application ----------------------------- #
    
    def run(self):
        """ Runs the program with the provided background object. """
        while self.button != 'Q':
            # Cipher Commands
            if self.button in "RPV":
                self.run_cipher()
            elif self.button == "B":
                self.run_benchmarks()
            # Input Commands
            elif self.button in "FIK":
                self.run_prompt()
            # Incorrect Command
            elif self.button != "startup":
                self.update_status("ERROR: Invalid menu selection!")
                self.background.refresh()
            
            self.button = self.background.getkey().upper()

    def run_prompt(self):
        """Handle the current input command."""
        if self.button == 'F':
            prompt = "Enter file to load, then press [ENTER]"
            command = self.read_from_file
            status_cancel = "File load cancelled."
        elif self.button == 'I':
            prompt = "Enter new text below, then press [ENTER]"
            command = self.read_from_input
            status_cancel = "Cancelled user input of text (empty string)."
        elif self.button == 'K':
            prompt = "Enter new key and then press [ENTER]"
            command = self.change_cipher_key
            status_cancel = "Cancelled user input of key (empty string)."
        
        self.update_prompt(prompt)
        self.prompt.refresh()

        user_input = self.get_user_input()
        if user_input == "":
            self.update_status(status_cancel)
            self.prompt.clear()
            self.prompt.refresh()
            self.background.refresh()
            return

        status_output = command(user_input)
        self.update_status(status_output)

        self.prompt.clear()
        self.prompt.refresh()
        self.background.refresh()
    
    def get_user_input(self):
        self.input.box()
        self.input.refresh() # No need to clear, prompt clears this

        self.textwin.clear()
        self.textwin.move(0, 0)
        textbox = Textbox(self.textwin)
        textbox.edit()

        user_input = textbox.gather()
        user_input = user_input[0:len(user_input) - 1]
        
        return user_input.strip()
    
    def run_cipher(self):
        pass

    
    # ------------------------------ Input Commands ------------------------------ #

    def read_from_file(self, file: str):
        """
        Read text from a local file.
        
        Parameters:
        file: The relative path to the file to be ciphered.
        """
        return "File contents loaded successfully."

    def read_from_input(self, t: str):
        """
        Read text from user input prompt.

        Parameters:
        t: The text to replace with.
        """
        self.text = t.encode('cp437')
        self.update_text_and_key()
        self.output.refresh()
        return "New text loaded into memory from user input."

    def change_cipher_key(self, k: str):
        """
        Change key used for ciphers.
        
        Parameters:
        k: The key to replace with.
        """
        self.key = k.encode('cp437')
        self.update_text_and_key()
        self.output.refresh()
        return "New key loaded into memory from user input."

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
        self.update_prompt("Running benchmarks...")
        self.prompt.refresh()

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
            
    def update_status(self, status):
        """Update the status shown."""
        self.background.addstr(self.OVERLAY_ROWS, 0, " " * self.OUTPUT_COLS)
        self.background.addstr(self.OVERLAY_ROWS, 0, "Status: " + status)
    
    def update_prompt(self, message):
        """Update the prompt shown"""
        x = self.PROMPT_COLS // 2 - len(message) // 2 # Center text
        self.prompt.addstr(1, x, message)
        self.prompt.box()
