from decode import decode
from encode import encode
from utils import scramble_random_position, generate_prime_number, scramble_random_position, from_base_p, write_number_into_file

if __name__ == '__main__':
    p = generate_prime_number(16)
    print("p = ", p)
    s = 1
    y = encode('input.txt', p, s)
    print("y = ", y)
    z = scramble_random_position(y, p)
    print("z = ", z)
    factors_decoded = decode(z, p, s)
    print("Factors after decoding are: ", [int(i) for i in factors_decoded])
    num = from_base_p(factors_decoded, p)
    print("File number after decoding: ", num)
    write_number_into_file('output.txt', int(num))