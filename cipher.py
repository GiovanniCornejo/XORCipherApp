import curses

def main():
    curses.wrapper(run_gui)
    print("Thanks for using the XOR-Cipher App; See you next time!")

# -----------------------CIPHER----------------------- #

def cipher(message: bytes, key: bytes) -> bytes:
    """
    Executes the Python XOR-cipher.
    
    Parameters:
        message: The message to be ciphered.
        key: The key used for ciphering.
        
    Returns:
        bytes: The ciphered byte sequence.
    """
    return bytes([message[i] ^ key[i % len(key)] for i in range(0, len(message))])

def load_cipher_lib(library_path: str):
    """
    Loads the cipher shared library at the specified path, sets its method parameters,
    and returns the library object.
    
    Parameters:
        library_path: The path to the cipher shared library.
        
    Returns:
        object: The loaded cipher library object.
    """
    pass

# -----------------------GUI----------------------- #

def run_gui(background: curses.window):
    """
    Runs the program with the provided background object using curses.wrapper().
    
    Parameters:
        background (object): The background object.
        
    Returns:
        None
    """
    curses.curs_set(0) # No cursor
    curses.noecho() # Type without it showing
    curses.cbreak() # Cbreak to exit

    key = "But there's one sound that no one knows... What does the Fox say?".encode('cp437')
    text = "This is a haiku; it is not too long I think; but you may disagree".encode('cp437')

    overlay_window = print_overlay()

    # Run Application
    button = "startup"
    while button.lower() != 'q':
        background.clear()

        background.refresh()
        overlay_window.refresh()
        button = background.getkey()
        
def print_overlay():
    overlay_window = curses.newwin(24, 80, 0, 0)
    overlay_window.box()

    # Welcome Message
    _, w = overlay_window.getmaxyx()
    intro_message = "Welcome to the XOR-Cipher App!"
    x = w // 2 - len(intro_message) // 2
    y = 1
    overlay_window.addstr(y, x, intro_message)

    return overlay_window





if __name__ == "__main__":
    main()
