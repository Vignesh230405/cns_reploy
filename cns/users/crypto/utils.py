import random
import string

def generate_caesar_key():
    return random.randint(0, 25)


def generate_playfair_key(length=6):
    letters = string.ascii_uppercase.replace("J", "")
    return ''.join(random.sample(letters, length))

def _mod_inverse(a, m=26):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def generate_hill_key():
    while True:
        a = random.randint(0, 25)
        b = random.randint(0, 25)
        c = random.randint(0, 25)
        d = random.randint(0, 25)

        det = a * d - b * c
        if _mod_inverse(det, 26) is not None:
            return [[a, b], [c, d]]


def generate_key_for_algorithm(algorithm):
    if algorithm == "CAESAR":
        return generate_caesar_key()

    if algorithm == "PLAYFAIR":
        return generate_playfair_key()

    if algorithm == "HILL":
        return generate_hill_key()

    raise ValueError("Unknown algorithm")
