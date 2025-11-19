from .utils import generate_key_for_algorithm, _mod_inverse


# ---------------------- CAESAR ----------------------

def caesar_encrypt(text):
    key = generate_key_for_algorithm("CAESAR")
    text = text.upper()
    result = []

    for ch in text:
        if 'A' <= ch <= 'Z':
            num = ord(ch) - 65
            num = (num + key) % 26
            result.append(chr(num + 65))
        else:
            result.append(ch)

    return ''.join(result), key


def caesar_decrypt(text, key):
    text = text.upper()
    result = []

    for ch in text:
        if 'A' <= ch <= 'Z':
            num = ord(ch) - 65
            num = (num - key) % 26
            result.append(chr(num + 65))
        else:
            result.append(ch)

    return ''.join(result)


# ---------------------- PLAYFAIR ----------------------

def _playfair_generate_key_square(key):
    key = key.upper().replace("J", "I")
    used = set()
    table = []

    for ch in key:
        if 'A' <= ch <= 'Z' and ch not in used:
            used.add(ch)
            table.append(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in used:
            used.add(ch)
            table.append(ch)

    return [table[i*5:(i+1)*5] for i in range(5)]


def _playfair_find(table, ch):
    for r in range(5):
        for c in range(5):
            if table[r][c] == ch:
                return r, c
    return None


def _playfair_prepare(text):
    text = text.upper().replace("J", "I")
    cleaned = [ch for ch in text if 'A' <= ch <= 'Z']

    pairs = []
    i = 0
    while i < len(cleaned):
        a = cleaned[i]
        b = cleaned[i+1] if i + 1 < len(cleaned) else 'X'

        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2

    if len(pairs[-1]) != 2:
        pairs[-1] = (pairs[-1][0], 'X')

    return pairs


def playfair_encrypt(text):
    key = generate_key_for_algorithm("PLAYFAIR")
    table = _playfair_generate_key_square(key)
    pairs = _playfair_prepare(text)
    result = []

    for a, b in pairs:
        r1, c1 = _playfair_find(table, a)
        r2, c2 = _playfair_find(table, b)

        if r1 == r2:
            result.append(table[r1][(c1 + 1) % 5])
            result.append(table[r2][(c2 + 1) % 5])

        elif c1 == c2:
            result.append(table[(r1 + 1) % 5][c1])
            result.append(table[(r2 + 1) % 5][c2])

        else:
            result.append(table[r1][c2])
            result.append(table[r2][c1])

    return ''.join(result), key


def playfair_decrypt(text, key):
    table = _playfair_generate_key_square(key)
    text = text.upper()
    pairs = [(text[i], text[i+1]) for i in range(0, len(text), 2)]
    result = []

    for a, b in pairs:
        r1, c1 = _playfair_find(table, a)
        r2, c2 = _playfair_find(table, b)

        if r1 == r2:
            result.append(table[r1][(c1 - 1) % 5])
            result.append(table[r2][(c2 - 1) % 5])

        elif c1 == c2:
            result.append(table[(r1 - 1) % 5][c1])
            result.append(table[(r2 - 1) % 5][c2])

        else:
            result.append(table[r1][c2])
            result.append(table[r2][c1])

    return ''.join(result)

# ---------------------- HILL (2x2) ----------------------


def _hill_prepare(text):
    text = ''.join(ch for ch in text.upper() if 'A' <= ch <= 'Z')
    return text


def hill_encrypt(text):
    key_matrix = generate_key_for_algorithm("HILL")
    text = _hill_prepare(text)

    # Determine if padding needed
    pad_flag = 0
    if len(text) % 2 != 0:
        text += 'X'
        pad_flag = 1

    result = []

    for i in range(0, len(text), 2):
        p1 = ord(text[i]) - 65
        p2 = ord(text[i+1]) - 65

        c1 = (key_matrix[0][0]*p1 + key_matrix[0][1]*p2) % 26
        c2 = (key_matrix[1][0]*p1 + key_matrix[1][1]*p2) % 26

        result.append(chr(c1 + 65))
        result.append(chr(c2 + 65))

    encrypted = ''.join(result)

    # Append flag at end
    encrypted += str(pad_flag)

    return encrypted, key_matrix


def hill_decrypt(text, key_matrix):
    # Extract padding flag
    pad_flag = int(text[-1])
    text = text[:-1]  # remove flag

    # Clean text
    text = ''.join(ch for ch in text.upper() if 'A' <= ch <= 'Z')

    a, b = key_matrix[0]
    c, d = key_matrix[1]

    det = a*d - b*c
    det_inv = _mod_inverse(det, 26)
    if det_inv is None:
        raise ValueError("Key matrix not invertible mod 26")

    inv_matrix = [
        [(d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, (a * det_inv) % 26]
    ]

    result = []

    for i in range(0, len(text), 2):
        c1 = ord(text[i]) - 65
        c2 = ord(text[i+1]) - 65

        p1 = (inv_matrix[0][0]*c1 + inv_matrix[0][1]*c2) % 26
        p2 = (inv_matrix[1][0]*c1 + inv_matrix[1][1]*c2) % 26

        result.append(chr(p1 + 65))
        result.append(chr(p2 + 65))

    plaintext = ''.join(result)

    # Remove padding if it was added
    if pad_flag == 1:
        plaintext = plaintext[:-1]

    return plaintext

# ---------------------- WRAPPERS ----------------------

SUPPORTED_ALGORITHMS = {"CAESAR", "PLAYFAIR", "HILL"}


def encrypt(plaintext, algorithm):
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError("Unsupported algorithm")

    if algorithm == "CAESAR":
        return caesar_encrypt(plaintext)

    if algorithm == "PLAYFAIR":
        return playfair_encrypt(plaintext)

    if algorithm == "HILL":
        return hill_encrypt(plaintext)

    raise ValueError("Unknown algorithm")


def decrypt(ciphertext, algorithm, key):
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError("Unsupported algorithm")

    if algorithm == "CAESAR":
        return caesar_decrypt(ciphertext, int(key))

    if algorithm == "PLAYFAIR":
        return playfair_decrypt(ciphertext, key)

    if algorithm == "HILL":
        return hill_decrypt(ciphertext, key)

    raise ValueError("Unknown algorithm")

#this is for testing
#pas, key = encrypt("JINX", "HILL")
#print(pas, key)
#raw_pass = decrypt(pas, "HILL", key)
#print(raw_pass)