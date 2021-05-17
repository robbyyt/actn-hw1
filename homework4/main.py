from sympy import randprime, isprime, gcd
from random import randint

def generate_usable_prime(bit_number=512):
    q = randprime(2**(bit_number-1), 2 ** bit_number)
    p = 2 * q + 1
    while not isprime(p):
        q = randprime(2 ** (bit_number - 1), 2 ** bit_number)
        p = 2 * q + 1

    return p, q

def generate_random_coprime_number(p):
    a = randint(0, p - 1)

    while gcd(a, p) != 1:
        a = randint(0, p-1)

    return a

def legendre_jacobi(a, n):
    t = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            if n % 8 in [3, 5]:
                t = -t
        a, n = n, a
        


def generate_quadratic_non_residue(p):
    if p % 4 == 3:
        return p-1
    if p % 8 == 5:
        return 2

    a = generate_quadratic_non_residue(p)



if __name__ == '__main__':
