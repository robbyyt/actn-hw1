from utils import read_file_into_number, to_base_p, generate_prime_number, compute_modular_polynomial


def encode(file, p, s):
    num = read_file_into_number(file)
    factors = to_base_p(num, p)
    k = len(factors) + 1
    n = k + 2 * s
    to_send = []
    print(factors)
    for i in range(1, n + 1):
        to_send.append(compute_modular_polynomial(factors, i, p))


if __name__ == '__main__':
    p = generate_prime_number(80)
    s = 1
    print(encode('input.txt', p, s))
