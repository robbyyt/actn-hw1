from random import sample
import numpy as np
from utils import compute_modular_inverse, compute_negative_modular_product,  compute_modular_sum
from itertools import combinations
from time import time


def compute_fc_naive(a, z, p):
    sum = 0
    for i in a:
        sum += z[i - 1] * np.prod([j * compute_modular_inverse(j - i, p) for j in (a - {i})]) % p
        sum %= p
    return sum


def compute_fc_k_inversions(a, z, p):
    sum = 0
    for i in a:
        sum += z[i - 1] * (np.prod([j for j in (a - {i})]) % p) * \
               compute_modular_inverse(np.prod([j - i for j in (a - {i})]) % p, p)
        sum %= p

    return sum


# def compute_fc_one_inversion(a, z, p):
#     terms = []
#     for i in a:
#         terms.append(
#             (z[i - 1] * np.prod([j for j in (a - {i})]) % p,
#              np.prod([(j - i) % p for j in (a - {i})]) % p
#              )
#         )
#
#     numerator = 0
#     denominator = 1
#     for i in range(len(terms)):
#         to_add = terms[i][0]
#         for j in range(len(terms)):
#             if i != j:
#                 to_add = (to_add * terms[j][1]) % p
#
#         numerator += to_add
#         numerator %= p
#         denominator *= terms[i][1]
#         denominator %= p
#
#     return (numerator * compute_modular_inverse(denominator, p)) % p

def compute_fc_one_inversion(a, z, p):
    # numaratori
    numerators = []
    # numitori
    denominators = []

    for i in a:
        numerator = z[i - 1]
        denominator = 1
        for j in a:
            if i != j:
                numerator *= j
                numerator %= p
                denominator *= (j - i) % p
                denominator %= p

        numerators.append(numerator)
        denominators.append(denominator)

    # aducerea la numitor comun
    sum = 0
    divide_by = 1
    for i in range(len(numerators)):
        to_add = numerators[i]
        for j in range(len(denominators)):
            if i != j:
                to_add *= denominators[j]
                to_add %= p
        sum += to_add
        sum %= p
        divide_by *= denominators[i]
        divide_by %= p

    return sum * compute_modular_inverse(divide_by, p) % p


# def interpolate_polynomial(a, z, p):
#     result = np.zeros(len(a) - 1)
#     initial_coefs = []
#
#     for i in a:
#         initial_coefs.append(z[i - 1] * compute_modular_inverse(np.prod([(i - j) % p for j in (a - {i})]) % p, p) % p)
#
#     for i in range(len(result)):
#         for j in range(len(initial_coefs)):
#             if i == 0:
#                 result[i] += initial_coefs[j]
#                 result %= p
#             else:
#                 lst = list(a)
#                 comb_sum = 0
#                 for comb in combinations(a - {lst[j]}, i):
#                     print(comb)
#                     comb_sum += compute_negative_modular_product(comb, p)
#                     comb_sum %= p
#
#                 result[i] += initial_coefs[j] * comb_sum
#                 result[i] %= p
#
#     return result

def interpolate_polynomial(a, z, p, k):
    result = np.zeros(k - 1)
    a_list = list(a)
    coefs = []
    for i in range(k):
        coefs.append(z[a_list[i] - 1])

    for index, i in enumerate(a_list):
        divide_by = 1
        for j in a_list:
            if i != j:
                divide_by *= i - j
                divide_by %= p
        coefs[index] *= compute_modular_inverse(divide_by, p)
        coefs[index] %= p

    result[0] = compute_modular_sum(coefs, p)

    for index, i in enumerate(a_list):
        current = a - {i}
        for step in range(1, len(result)):
            combs = list(combinations(current, step))
            prods = [compute_negative_modular_product(subset, p) for subset in combs]
            sum = compute_modular_sum(prods, p)
            result[step] += (coefs[index] * sum) % p
            result[step] %= p

    return result









def decode(z, p, s):
    n = len(z)
    k = n - 2 * s
    indexes = {i + 1 for i in range(n)}
    print("Indexes: ", indexes)
    f_c = 1

    while f_c != 0:
        a = set(sample(indexes, k))
        start = time()
        # f_c = compute_fc_naive(a, z, p)
        # f_c = compute_fc_k_inversions(a, z, p)
        f_c = compute_fc_one_inversion(a, z, p)
        end = time()
        print("Computed f_c in: %f" % (end - start))
        print("A = ", a)
        print("f_c = ", f_c)

    return interpolate_polynomial(a, z, p, k)


if __name__ == '__main__':
    z = [9, 2, 6, 5, 8]
    p = 11
    result = decode(z, 11, 1)
    print(result)
