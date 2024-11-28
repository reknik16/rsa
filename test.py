import random
from main import RSA, MathCalculator, PrimeGenerator
import pytest


class TestRSA:
    def test_rsa_generation(self):
        rsa_gen = RSA()
        e, d, n, p, q = rsa_gen.generate_key_rsa(10 ** 57)
        M = random.randrange(0, n)
        sign = MathCalculator.pow(M, d, p, q)

        check = MathCalculator.pow(sign, e, p, q)
        assert check == M

    @pytest.mark.parametrize(
        "number, degree, mod1, mod2, expected",
        [(2, 10, 3, 5, 4), (3, 2, 2, 3, 1), (2, 10, 2, 5, 9)]
    )
    def test_get_pow(self, number, degree, mod1, mod2, expected):
        result = MathCalculator.pow(number, degree, mod1, mod2)
        assert result == expected

    def test_pow_raise_exception(self):
        with pytest.raises(ZeroDivisionError):
            MathCalculator.pow(15, 2, 0, 1)

    def test_is_prime(self):
        rand = random.randint(0, 90)
        prime_gen = PrimeGenerator(100000)
        assert prime_gen.is_prime(prime_gen.get_prime_by_number(rand))

    def test_is_prime_raise_exception(self):
        n = 100000
        prime_gen = PrimeGenerator(n)
        with pytest.raises(Exception):
            prime_gen.get_prime_by_number(n)

    def test_extended_euclid(self):
        result = MathCalculator.extended_euclid(35, 15)
        assert (5, 1, -2) == result

    def test_rabin_muller(self):
        generator = PrimeGenerator(3000)
        prime = generator.generate_prime(50)
        assert generator.rabin_miller(prime, 30)
