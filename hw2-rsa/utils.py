from sympy.ntheory.generate import randprime
from random import randint


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def binary_gcd_inner(u, v, x_1, y_1, a, b, c, d, g):
    while u % 2 == 0:
        u //= 2
        if a % 2 == b % 2 == 0:
            a //= 2
            b //= 2
        else:
            a = (a + y_1) // 2
            b = (b - x_1) // 2

    while v % 2 == 0:
        v //= 2
        if c % 2 == d % 2 == 0:
            c //= 2
            d //= 2
        else:
            c = (c + y_1) // 2
            d = (d - x_1) // 2

    if u >= v:
        u -= v
        a -= c
        b -= d
    else:
        v -= u
        c -= a
        d -= b

    if u == 0:
        return c, d, g * v
    else:
        return binary_gcd_inner(u, v, x_1, y_1, a, b, c, d, g)


def extended_binary_gcd(x, y):
    g = 1
    u = x
    v = y
    while u % 2 == 0 and v % 2 == 0:
        u //= 2
        v //= 2
        g *= 2

    x_1 = u
    y_1 = v
    a = d = 1
    b = c = 0

    return binary_gcd_inner(u, v, x_1, y_1, a, b, c, d, g)


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


def modular_multiplicative_inverse_binary(a, modulo):
    x, y, cmmdc = extended_binary_gcd(modulo, a)
    if cmmdc != 1:
        return False

    return y


def generate_public_exponent(phi, e_bit_number=32):
    e = randint(2, 2 ** e_bit_number)
    while gcd(phi, e) != 1:
        e = randint(2, e_bit_number)
    return e


def generate_multiprime_rsa_key(bit_number=512, e_bit_number=32):
    p = randprime(2 ** (bit_number - 1), 2 ** bit_number)
    q = randprime(2 ** (bit_number - 1), 2 ** bit_number)
    r = randprime(2 ** (bit_number - 1), 2 ** bit_number)
    phi = (p - 1) * (q - 1) * (r - 1)
    e = generate_public_exponent(phi, e_bit_number)
    d = modular_multiplicative_inverse(e, phi)

    return p, q, r, e, d


def decrypt_multiprime_using_tcr(enc, p, q, r, d):
    n_array = [p, q, r]
    y_array = [q * r, p * r, p * q]
    z_array = [modular_multiplicative_inverse(y_array[i], n_array[i]) for i in range(len(n_array))]
    x_array = [pow(enc % f, d % (f - 1), f) for f in n_array]

    return sum([x_array[i] * y_array[i] * z_array[i] for i in range(len(n_array))]) % (p * q * r)


def generate_multipower_rsa_key(bit_number=512, e_bit_number=32):
    p = randprime(2 ** (bit_number - 1), 2 ** bit_number)
    q = randprime(2 ** (bit_number - 1), 2 ** bit_number)
    phi = p * (p - 1) * (q - 1)
    e = generate_public_exponent(phi, e_bit_number)
    d = modular_multiplicative_inverse(e, phi)

    return p, q, e, d


def modular_sum(arr, modulo):
    sum = 0
    for el in arr:
        sum += el
        sum %= modulo
    return sum


def decrypt_multipower_using_tcr(enc, p, q, d, e):
    n_array = [p ** 2, q]
    y_array = [q, p ** 2]
    z_array = [modular_multiplicative_inverse(y_array[i], n_array[i]) for i in range(len(n_array))]
    x_q = pow(enc % q, d % (q - 1), q)
    x_0 = pow(enc % p, d % (p - 1), p)
    x_1 = ((enc - pow(x_0, e, p ** 2)) // p) * modular_multiplicative_inverse((e * pow(x_0, e - 1, p)) % p, p)
    x_1 %= p
    x_array = [p * x_1 + x_0, x_q]

    return modular_sum([x_array[i] * y_array[i] * z_array[i] for i in range(len(n_array))], p ** 2 * q)


def lr_sliding_window(x, n, m, w=3):
    x_dict = {1: x % m, 2: pow(x, 2, m)}
    for v in range(3, 2 ** w, 2):
        x_dict[v] = (x_dict[v - 2] * x_dict[2]) % m

    # reversed n_bin so n_k-1 is last
    # print(bin(n))
    n_bin = bin(n)[2:][::-1]
    y = 1
    i = len(n_bin) - 1
    windows = []
    while i >= 0:
        if n_bin[i] == '0':
            y = (y * y) % m
            # print(n_bin[i])
            windows.append(n_bin[i])
            i -= 1
        else:
            best_j = i
            j_next = i - 1
            while i - j_next + 1 <= w and j_next >= 0:
                if n_bin[j_next] == '1':
                    best_j = j_next
                j_next -= 1

            windows.append(n_bin[best_j:i+1][::-1])
            for l in range(1, i - best_j + 2):
                y = (y * y) % m
            y = (y * x_dict[get_number_from_bitstring(n_bin[best_j:i+1][::-1])]) % m
            i = best_j - 1

    return y, windows


def get_number_from_bitstring(bs):
    return int(bs, 2)


def get_additive_chain_from_windows(windows, n, w=3):
    chain = [1, 2]
    for i in range(3, 2 ** w, 2):
        chain.append(i)

    current = get_number_from_bitstring(windows[0])

    for i in range(1, len(windows)):
        if windows[i] == '0':
            current *= 2
            chain.append(current)
            if current == n:
                return chain
        else:
            for l in range(1, len(windows[i]) + 1):
                current *= 2
                chain.append(current)
                if current == n:
                    return chain
            current += get_number_from_bitstring(windows[i])
            chain.append(current)
            if current == n:
                return chain
    return chain


def decrypt_multiprime_using_tcr_ex3_v1(enc, p, q, r, d):
    n_array = [p, q, r]
    y_array = [q * r, p * r, p * q]
    z_array = [modular_multiplicative_inverse(y_array[i], n_array[i]) for i in range(len(n_array))]
    x_array = [lr_sliding_window(enc % f, d % (f - 1), f)[0] for f in n_array]

    return sum([x_array[i] * y_array[i] * z_array[i] for i in range(len(n_array))]) % (p * q * r)


def decrypt_multiprime_using_tcr_ex3_v2(enc, p, q, r, d, chain_p, chain_q, chain_r, f2wp, f2wq, f2wr):
    n_array = [p, q, r]
    y_array = [q * r, p * r, p * q]
    z_array = [modular_multiplicative_inverse(y_array[i], n_array[i]) for i in range(len(n_array))]
    x_array = [
        exponentiate_using_additive_chain(enc % p, chain_p, p, f2wp),
        exponentiate_using_additive_chain(enc % q, chain_q, q, f2wq),
        exponentiate_using_additive_chain(enc % r, chain_r, r, f2wr)
    ]
    return sum([x_array[i] * y_array[i] * z_array[i] for i in range(len(n_array))]) % (p * q * r)


def get_first_2w_results(x, m, w=3):
    x_dict = {1: x % m, 2: pow(x, 2, m)}
    for v in range(3, 2 ** w, 2):
        x_dict[v] = (x_dict[v - 2] * x_dict[2]) % m

    return x_dict


def exponentiate_using_additive_chain(x, chain, m, first_2w_results, w=3):
    result = first_2w_results[chain[2 ** (w - 1) + 1] // 2] ** 2 % m

    for i in range(2 ** (w - 1) + 2, len(chain)):
        if chain[i] == 2 * chain[i - 1]:
            result = pow(result, 2, m)
        else:
            result = result * first_2w_results[chain[i] - chain[i - 1]] % m

    return result


if __name__ == '__main__':
    y, windows = lr_sliding_window(3, 8035684709982418161771646911529190986598061775700958149950501435295752769055012803954666633272389956140405312786769193907761753931423510958481004801704937, 500)
    print(windows)
    print(y)
    print(pow(3, 8035684709982418161771646911529190986598061775700958149950501435295752769055012803954666633272389956140405312786769193907761753931423510958481004801704937, 500))
    print(get_additive_chain_from_windows(windows, 8035684709982418161771646911529190986598061775700958149950501435295752769055012803954666633272389956140405312786769193907761753931423510958481004801704937))
