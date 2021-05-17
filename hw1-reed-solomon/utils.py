from sympy.ntheory.generate import randprime
from random import randrange
import numpy as np


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


def scramble_random_position(arr, p):
    random_index = randrange(len(arr))
    new_value = randrange(p)

    while new_value == arr[random_index]:
        new_value = randrange(p)

    new = arr.copy()
    new[random_index] = new_value

    return new


def compute_modular_inverse(a, p):
    return a ** (p - 2) % p


def compute_negative_modular_product(arr, p):
    product = 1
    for i in arr:
        product *= -i
        product %= p

    return product


def compute_modular_sum(arr, p):
    suma = 0
    for i in arr:
        suma += i
        suma %= p

    return suma


def from_base_p(factors, p):
    power = 1
    num = 0
    for f in reversed(factors):
        num += int(f) * power
        power *= p

    return num


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def write_number_into_file(file, num):
    output = int_to_bytes(num)

    with open(file, 'wb') as f:
        f.write(output)




