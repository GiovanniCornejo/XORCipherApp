/// Executes the Rust-based cipher. The cipher-text is written to `buf` by applying XOR to `key` and `msg`.
///
/// # Arguments
///
/// * `msg` - A pointer to the message to be ciphered.
/// * `key` - A pointer to the key used for ciphering.
/// * `buf` - A pointer to the buffer where the ciphered text will be written.
/// * `msg_len` - The length of the message.
/// * `key_len` - The length of the key.
///
/// # Safety
///
/// This function is marked as unsafe because it deals with raw pointers.
/// It's the caller's responsibility to ensure that the pointers are valid and that
/// the memory they point to is properly allocated and mutable.
///
#[no_mangle]
pub fn cipher(msg: *const i8, key: *const i8, buf: *mut i8, msg_len: usize, key_len: usize) {
    unsafe {
        for i in 0..msg_len as isize {
            *buf.offset(i) = *msg.offset(i) ^ *key.offset(i % key_len as isize);
        }
    }
}
