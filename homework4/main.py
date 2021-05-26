from sympy import randprime, isprime, gcd
from random import randint
from math import sqrt, ceil
from sympy.ntheory import discrete_log, is_primitive_root
from sympy.ntheory.residue_ntheory import primitive_root
import numpy as np


def modular_multiplicative_inverse(a, modulo):
    x = 0
    x0 = 1
    r = modulo
    r0 = a

    while r0 != 0:
        quotient = r // r0
        x, x0 = x0, x - quotient * x0
        r, r0 = r0, r - quotient * r0

    if r > 1:
        # r > 1 means that input does not have an inverse.
        return False
    if x < 0:
        x += modulo

    return x


def generate_usable_prime(bit_number=512):
    q = randprime(2 ** (bit_number - 1), 2 ** bit_number)
    p = 2 * q + 1
    while not isprime(p):
        q = randprime(2 ** (bit_number - 1), 2 ** bit_number)
        p = 2 * q + 1

    return p, q


def generate_random_coprime_number(p):
    a = randint(0, p - 1)

    while gcd(a, p) != 1:
        a = randint(0, p - 1)

    return a


def legendre_jacobi(a, n):
    t = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            if n % 8 in [3, 5]:
                t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a = a % n

    return t


def generate_quadratic_non_residue(p):
    if p % 4 == 3:
        return p - 1
    if p % 8 == 5:
        return 2

    a = generate_random_coprime_number(p)

    while legendre_jacobi(a, p) != -1:
        a = generate_random_coprime_number(p)

    return a


# p = 2q + 1
def generate_primitive_root(p):
    y = randint(2, p - 2)
    a = -pow(y, 2, p) % p

    return a


def generate_primitive_root_2(p, factors):
    alpha = generate_quadratic_non_residue(p)
    ok = True
    for f, e in factors:
        if f != 2:
            if pow(alpha, (p - 1) // f, p) == 1:
                ok = False

    if ok:
        return alpha


def get_discrete_log_shanks(p, beta, alpha):
    m = ceil(sqrt(p - 1))
    table = []
    for j in range(0, m):
        table.append((pow(alpha, j, p), j))
    table.sort(key=lambda x: x[0])
    table = dict(table)

    multiply_by = pow(modular_multiplicative_inverse(alpha, p), m, p)
    y = beta

    for i in range(0, m):
        if y in table:
            return (i * m + table[y]) % p
        y *= multiply_by
        y %= p


def solve_tcr(a_array, n_array):
    n = np.prod(n_array)

    y_array = []
    for i in range(len(n_array)):
        y_array.append(n // n_array[i])

    z_array = []
    for i in range(len(n_array)):
        z_array.append(modular_multiplicative_inverse(y_array[i], n_array[i]))

    return sum([a_array[i] * y_array[i] * z_array[i] for i in range(len(n_array))]) % n


def get_discrete_log_sph(p, beta, alpha, factors):
    x_array = []
    for i in range(len(factors)):
        q = factors[i][0]
        e = factors[i][1]

        y = 1

        alpha_current = pow(alpha, p // q, p)
        l_array = [0]

        for j in range(e):
            y = y * pow(alpha, int(l_array[j] * (q ** (j - 1))), p)
            beta_current = pow(beta * modular_multiplicative_inverse(y, p), p // (q ** (j + 1)), p)
            l_array.append(discrete_log(p, beta_current, alpha_current))

        l_array.pop(0)
        x_current = 0
        current_pow = 1

        for l in l_array:
            x_current += l * current_pow
            current_pow *= q

        x_array.append(x_current % p)

    return solve_tcr(x_array, [factor[0] ** factor[1] for factor in factors])


if __name__ == '__main__':
    print("Shanks basic example")
    p = 113
    alpha = 3
    beta = 57

    res = get_discrete_log_shanks(p, beta, alpha)
    print(res)

    print("Shanks with 32 bit prime")
    p, q = generate_usable_prime(32)
    a = generate_quadratic_non_residue(p)
    g = generate_primitive_root(p)
    beta = randint(0, p - 1)
    print("ALPHA: ", g)
    print("BETA: ", beta)
    print("P: ", p)
    res = get_discrete_log_shanks(p, beta=beta, alpha=g)
    print(res)

    # SPH small
    print("SPH small")
    p = 251
    alpha = 71
    beta = 210
    factors = [(2, 1), (5, 3)]
    res = get_discrete_log_sph(p, beta, alpha, factors)
    print(res)

    # SPH big
    print("SPH big")
    p = 22708823198678103974314518195029102158525052496759285596453269189798311427475159776411276642277139650833937
    factors = [(2, 4), (104729, 8), (224737, 8), (350377, 4)]
    alpha = generate_primitive_root_2(p, factors)
    while not is_primitive_root(alpha, p):
        alpha = generate_primitive_root_2(p, factors)
    # alpha = primitive_root(p)

    beta = randint(0, p - 1)
    print("ALPHA: ", alpha)
    print("BETA: ", beta)
    res = get_discrete_log_sph(p, beta, alpha, factors)
    print(res)