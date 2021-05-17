from random import randint
from math import sqrt


def lucas_lehmer(s, trial_steps=5):
    n = 2 ** s - 1
    if s > 3:
        for _ in range(trial_steps):
            a = randint(2, int(sqrt(s)))
            if n % a == 0:
                return 'composite'

    u = 4
    for _ in range(1, s - 1):
        u = u ** 2 - 2
        u = modular_reduction(u, s)

    if u == 0:
        return 'prime'
    else:
        return 'composite'


def modular_reduction(a, s):
    a_bin = bin(a)[2:]
    a_bin = "0" * ((2 * s) - len(a_bin)) + a_bin
    a1, a0 = a_bin[:len(a_bin) // 2], a_bin[len(a_bin) // 2:]
    return (int(a1, 2) + int(a0, 2)) % (2 ** s - 1)


def get_s_for_mersennse(n):
    n_bin = bin(n)[2:]
    if '0' in n_bin:
        raise ValueError("Number is not Mersenne")
    else:
        return len(n_bin)


if __name__ == '__main__':
    print(lucas_lehmer(4))
    print(lucas_lehmer(5))
    print(lucas_lehmer(get_s_for_mersennse(8191)))
    print(lucas_lehmer(23))