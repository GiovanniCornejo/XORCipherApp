import curses
from curses.textpad import Textbox

import ctypes
from timeit import timeit

from cipher import cipher, load_cipher_lib

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

        self.key = "But there's one sound that no one knows... What does the Fox say?".encode('cp437')
        self.text = "This is a haiku; it is not too long I think; but you may disagree".encode('cp437')
        self.button = "startup"
        
        # Load External Cipher
        self.cipher_lib = load_cipher_lib("libxorcipher.so")

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
        window = curses.newwin(self.OVERLAY_ROWS, self.OVERLAY_COLS, 0, 0)
        window.box()

        message = "Welcome to the XOR-Cipher App!"
        x = self.OVERLAY_COLS // 2 - len(message) // 2 # Center text
        window.addstr(1, x, message)

        return window
    
    def init_menu(self):
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
        window = curses.newwin(self.OUTPUT_ROWS, self.OUTPUT_COLS, self.OUTPUT_Y, self.OUTPUT_X)
        window.box()
        return window
    
    def init_prompt(self):
        window = curses.newwin(self.PROMPT_ROWS, self.PROMPT_COLS, self.PROMPT_Y, self.PROMPT_X)
        return window
    
    def init_input(self):
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
                self.button = self.background.getkey().upper()
                # Clear benchmarks output after next action
                self.prompt.clear()
                self.prompt.refresh()
                continue
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
            prompt = "Enter file to load below, then press [ENTER]"
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

        # Check if cancelled
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
        """Get user input for provided prompt."""
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
        """Handle the current cipher command."""
        if self.button == 'P':
            command = self.apply_python_cipher
        elif self.button == 'R':
            command = self.apply_rust_cipher
        elif self.button == 'V':
            command = self.verify_cipher_results
        
        status_output = command()
        self.update_status(status_output)
        self.background.refresh()
    
    # ------------------------------ Input Commands ------------------------------ #

    def read_from_file(self, file: str):
        """
        Read text from a local file.
        
        Parameters:
        file: The relative path to the file to be ciphered.
        """
        try:
            with open(file, 'r', encoding='cp437') as f:
                self.text = f.read().encode('cp437')
            self.update_text_and_key()
            self.output.refresh()
            return "File contents loaded successfully."
        except:
            return "ERROR: COULD NOT LOAD FILE: " + file

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
        self.cipher_lib.cipher(self.text, self.key, self.text, len(self.text), len(self.key))
        self.update_text_and_key()
        self.output.refresh()
        return "Applied Rust cipher."

    def apply_python_cipher(self):
        """Apply Python cipher to text"""
        self.text = cipher(self.text, self.key)
        self.update_text_and_key()
        self.output.refresh()
        return "Applied Python cipher."

    def verify_cipher_results(self):
        """
        The current text and key are ran through both ciphers and 
        the results are compared to verify that the cipher-text from each match one another. 
        """
        python_cipher = cipher(self.text, self.key)
        rust_cipher = ctypes.create_string_buffer(len(self.text))
        self.cipher_lib.cipher(self.text, self.key, rust_cipher, len(self.text), len(self.key))

        if python_cipher == bytes(rust_cipher):
            return "Cipher match verified!"
        else:
            return "WARNING: Ciphers do not match!"

    def run_benchmarks(self):
        """
        Run benchmarks on current text for Rust and Python cipher.
        To benchmark the ciphers, each is ran 100,000 times using the timeit module.
        """
        self.update_prompt("Running benchmarks...")
        self.prompt.refresh()
        self.prompt.clear()

        rust_cipher = ctypes.create_string_buffer(len(self.text))
        rust_time = timeit(lambda: self.cipher_lib.cipher(self.text, self.key, rust_cipher, len(self.text), len(self.key)), number=100000)
        python_time = timeit(lambda: cipher(self.text, self.key), number=100000)

        # Format cipher time outputs
        python_time_formatted = "{:.3f}".format(python_time)
        rust_time_formatted = "{:.3f}".format(rust_time)

        benchmark_output = "Results from Benchmark"
        x = self.PROMPT_COLS // 2 - len(benchmark_output) // 2 # Center text
        self.prompt.addstr(1, x, benchmark_output)
        self.prompt.addstr(2, x, "----------------------")
        self.prompt.addstr(3, x, f"Rust Cipher:   {rust_time_formatted:0>6s}s")
        self.prompt.addstr(4, x, f"Python Cipher: {python_time_formatted:0>6s}s")
        self.prompt.box()
        self.prompt.refresh()
        self.update_status("Benchmark results displayed.")
        self.background.refresh()

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
            
    def update_status(self, status: str):
        """Update the status shown."""
        self.background.addstr(self.OVERLAY_ROWS, 0, " " * self.OUTPUT_COLS)
        self.background.addstr(self.OVERLAY_ROWS, 0, "Status: " + status)
    
    def update_prompt(self, message: str):
        """Update the prompt shown"""
        x = self.PROMPT_COLS // 2 - len(message) // 2 # Center text
        self.prompt.addstr(1, x, message)
        self.prompt.box()
