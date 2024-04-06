import os
import ctypes

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
    full_library_path = os.path.abspath(library_path)
    libxorcipher = ctypes.cdll.LoadLibrary(full_library_path)
    libxorcipher.cipher.argtypes = (
        ctypes.c_char_p,  # msg
        ctypes.c_char_p,  # key
        ctypes.c_char_p,  # buf
        ctypes.c_size_t,  # msg_len
        ctypes.c_size_t   # key_len
    )

    return libxorcipher