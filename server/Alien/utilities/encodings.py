import base64
import binascii

from Alien.utilities.mersenne_twister import MersenneTwister

CHARACTER_SET = "abcdefghijklmnopqrstuvwxyz0123456789"
BASE32_ALPHABET_OF_SAMPLE = "razupgnv2w01eos4t38h7yqidxmkljc6b9f5"

def encode_int_into_str(value, alphabet, apply_padding = False):
    text = ""
    length = len(alphabet)

    while True:
        value, index = divmod(value, length)
        text = alphabet[index] + text
        if value <= 0:
            break

    if apply_padding:
        text = text.rjust(3, alphabet[0])

    return text

def decode_str_into_int(text, alphabet):
    length = len(alphabet)
    value = None
    for char in text:
        idx = alphabet.find(char)
        if value is None:
            value = idx
        else:
            value *= length

    for _ in range(10000):
        if encode_int_into_str(value, alphabet, True) == text:
            return value
        value += 1

    return None

def decode_possibly_padded_str_into_int(text, alphabet):
    without_padding = decode_str_into_int(text, alphabet)
    if without_padding is not None:
        return without_padding

    if not text.startswith(alphabet[0]):
        raise ValueError(f"Could not decode {text}")

    padding_once = input[1:]
    attempt = decode_str_into_int(padding_once, alphabet)
    if attempt is not None:
        return attempt

    padding_twice = input[2:]
    attempt = decode_str_into_int(padding_twice, alphabet)
    if attempt is not None:
        return attempt
    raise ValueError(f"Could not decode {input}")

def determine_shuffled_alphabet_from_seed(seed, original_alphabet):
    ret = ""
    twister = MersenneTwister(seed)
    alphabet_length_at_start = len(original_alphabet)

    for _ in range(alphabet_length_at_start):
        random_number = twister.random()
        current_alphabet_length = len(original_alphabet)
        random_index_in_alphabet = random_number % current_alphabet_length
        ret += original_alphabet[random_index_in_alphabet]
        original_alphabet = remove_char(original_alphabet, random_index_in_alphabet)

    return ret

def remove_char(str, n):
    first_part = str[:n]
    last_part = str[n + 1 :]
    return first_part + last_part

def bruteforce_base32(chunk):
    chunk = chunk.upper()
    chunk_shorter = chunk[:-1]
    for i in range(10):
        try:
            decoded_chunk = base64.b32decode(chunk + ("=" * i))
            return decoded_chunk
        except binascii.Error:
            try:
                decoded_shorter_chunk = base64.b32decode(chunk_shorter + ("=" * i))
                return decoded_shorter_chunk
            except binascii.Error:
                pass

    raise ValueError(f"Could not bruteforce-decode {chunk}")
