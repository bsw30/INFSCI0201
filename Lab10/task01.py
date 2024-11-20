# Task 01
def shift_character(char, shift, decrypt=False):
    shift = -shift if decrypt else shift
    if char.isupper():
        return chr((ord(char) - 65 + shift) % 26 + 65)
    elif char.islower():
        return chr((ord(char) - 97 + shift) % 26 + 97)
    return char  # Non-alphabetic characters remain unchanged

def caesar_cipher(text, shift, decrypt=False):
    """Encrypt or decrypt text using a Caesar Cipher with the given shift."""
    if not isinstance(shift, int):
        raise ValueError("Shift must be an integer.")
    return ''.join(shift_character(char, shift, decrypt) for char in text)

# Example usage:
if __name__ == "__main__":
    plaintext = "Hello World!"
    shift_key = 3
    encrypted_text = caesar_cipher(plaintext, shift_key)
    print("Encrypted:", encrypted_text)
    decrypted_text = caesar_cipher(encrypted_text, shift_key, decrypt=True)
    print("Decrypted:", decrypted_text)