import sys

def caesar_cipher(mode, text, shift):
    if not all(32 <= ord(char) <= 126 for char in text):
        raise ValueError("The script does not support your language yet.")

    if mode not in ("encode", "decode"):
        raise ValueError("Invalid mode. Use 'encode' or 'decode'.")

    if mode == "decode":
        shift = -shift

    shift = shift % 26
    result = []
    for char in text:
        if char.isalpha():
            alphabet_start = ord('a') if char.islower() else ord('A')
            new_index = (ord(char) - alphabet_start + shift) % 26
            result.append(chr(alphabet_start + new_index))
        else:
            result.append(char)

    return ''.join(result)

def main():
    if len(sys.argv) != 4:
        raise ValueError("Usage: python3 caesar.py <mode> <text> <shift>")

    mode = sys.argv[1]
    text = sys.argv[2]
    try:
        shift = int(sys.argv[3])
    except ValueError:
        raise ValueError("Shift must be an integer.")

    encoded_or_decoded_text = caesar_cipher(mode, text, shift)
    print(encoded_or_decoded_text)

if __name__ == '__main__':
    main()
