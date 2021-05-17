from utils import generate_multiprime_rsa_key, \
    decrypt_multiprime_using_tcr, generate_multipower_rsa_key, decrypt_multipower_using_tcr, decrypt_multiprime_using_tcr_ex3_v1, \
    decrypt_multiprime_using_tcr_ex3_v2, lr_sliding_window, get_additive_chain_from_windows, get_first_2w_results

from time import time
from random import randint


def print_statistics(time_array):
    time_ratio = [t[0] / t[1] for t in time_array]
    avg = sum(time_ratio) / len(time_ratio)
    print("On average, CRT decryption is %f faster" % avg)


def test_multiprime_decryption(iteration_number):
    times = []
    for i in range(iteration_number):
        p, q, r, e, d = generate_multiprime_rsa_key(1024)
        n = p * q * r
        msg = randint(0, n)
        enc = pow(msg, e, n)
        start = time()
        dec = pow(enc, d, n)
        end = time()
        normal_time = end - start
        start = time()
        dec = decrypt_multiprime_using_tcr(enc, p, q, r, d)
        end = time()
        crt_time = end - start
        times.append((normal_time, crt_time))
    return times


def test_multipower_decryption(iteration_number):
    times = []
    for i in range(iteration_number):
        p, q, e, d = generate_multipower_rsa_key(1024)
        n = p ** 2 * q
        msg = randint(0, n)
        enc = pow(msg, e, n)
        start = time()
        dec = pow(enc, d, n)
        end = time()
        normal_time = end - start
        start = time()
        dec = decrypt_multipower_using_tcr(enc, p, q, d, e)
        end = time()
        crt_time = end - start
        times.append((normal_time, crt_time))
    return times


def test_ex3_v1(iteration_number):
    times = []
    for i in range(iteration_number):
        p, q, r, e, d = generate_multiprime_rsa_key(1024)
        n = p * q * r
        msg = randint(0, n)
        enc = pow(msg, e, n)
        start = time()
        dec = pow(enc, d, n)
        end = time()
        normal_time = end - start
        start = time()
        dec = decrypt_multiprime_using_tcr_ex3_v1(enc, p, q, r, d)
        end = time()
        crt_time = end - start
        times.append((normal_time, crt_time))
    return times


def test_ex3_v2(iteration_number):
    times = []
    p, q, r, e, d = generate_multiprime_rsa_key(1024)
    n = p * q * r
    msg = 0
    windows_p = lr_sliding_window(msg % p, d % (p - 1), p)[1]
    windows_q = lr_sliding_window(msg % q, d % (q - 1), q)[1]
    windows_r = lr_sliding_window(msg % r, d % (r - 1), r)[1]
    chain_p = get_additive_chain_from_windows(windows_p, p)
    chain_q = get_additive_chain_from_windows(windows_q, q)
    chain_r = get_additive_chain_from_windows(windows_r, r)
    for i in range(iteration_number):
        msg = randint(0, n)
        enc = pow(msg, e, n)
        start = time()
        dec = pow(enc, d, n)
        end = time()
        normal_time = end - start
        start = time()
        f2wp = get_first_2w_results(enc % p, p)
        f2wq = get_first_2w_results(enc % p, q)
        f2wr = get_first_2w_results(enc % p, r)
        dec = decrypt_multiprime_using_tcr_ex3_v2(enc, p, q, r, d, chain_p, chain_q, chain_r, f2wp, f2wq, f2wr)
        end = time()
        crt_time = end - start
        times.append((normal_time, crt_time))

    return times


if __name__ == '__main__':
    num_iter = 100

    # multiprime
    multiprime_times = test_multiprime_decryption(num_iter)
    print("MULTIPRIME STATISTICS: ")
    print_statistics(multiprime_times)

    # multipower
    multipower_times = test_multipower_decryption(num_iter)
    print("MULTIPOWER STATISTICS: ")
    print_statistics(multipower_times)

    # ex 3
    ex3_times = test_ex3_v1(num_iter)
    print("EX3 STATS: ")
    print_statistics(ex3_times)

    # ex 3 v2
    ex2_v2_times = test_ex3_v2(num_iter)
    print("EX3 V2")
    print_statistics(ex2_v2_times)




