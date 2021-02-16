from sympy.ntheory.generate import randprime


def read_file_into_number(file):
    with open(file, 'rb') as f:
        content = f.read()
        return int.from_bytes(content, "big")


def generate_prime_number(bit_number):
    return randprime(2 ** (bit_number - 1), 2 ** bit_number)


def to_base_p(dec, p):
    number = dec
    remainders = []

    while number > 0:
        remainders.append(number % p)
        number = number // p

    remainders.reverse()

    return remainders


def compute_modular_polynomial(factors, x, p):
    result = 0

    for factor in factors:
        result = ((result + factor) * x) % p

    return result
