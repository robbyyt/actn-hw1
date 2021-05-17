from random import randint
from sympy.ntheory.generate import randprime


def compute_jacobi(a, n):
    assert (n > a > 0 and n % 2 == 1)
    s = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            r = n % 8
            if r == 3 or r == 5:
                s = -s
        a, n = n, a
        if a % 4 == n % 4 == 3:
            s = -s
        a %= n
    if n == 1:
        return s
    else:
        return 0


def expsign(sign, exp):

    if sign == 1:
        return 1
    assert sign == -1
    return -1 if exp % 2 else 1


def jacobi(m, n):
    assert n % 2 == 1
    if m == 2:
        if n % 8 in [1, 7]:
            return 1
        return -1
    m %= n
    q = 0
    while m & 1 == 0:
        m >>= 1
        q += 1
    if m == 1:
        return expsign(jacobi(2, n), q)
    return (expsign(jacobi(2, n), q)
            * (-1 if (n % 4 == 3) and (m % 4 == 3) else 1)
            * jacobi(n, m))


def solovay_strassen(n, tries):
    if n == 2:
        return "prime"
    if n % 2 == 0 or n < 2:
        return "composite"

    for i in range(tries):
        a = randint(2, n - 2)
        r = pow(a, (n - 1) // 2, n)
        if r != 1 and r != n - 1:
            return "composite"

        s = jacobi(a, n)
        if r != (s % n):
            return "composite"

    return "prime"


if __name__ == '__main__':
    p = randprime(2 ** 255, 2 ** 256 - 1)
    q = randprime(2 ** 255, 2 ** 256 - 1)
    print(solovay_strassen(p, 80))
    print(solovay_strassen(q, 80))
    print(solovay_strassen(p * q, 80))