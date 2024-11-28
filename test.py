import random
from main import RSA, MathCalculator
import pytest


class TestRSA:
    def test_rsa_generation(self):
        rsa_gen = RSA()
        e, d, n, p, q = rsa_gen.generate_key_rsa(10 ** 57)
        M = random.randrange(0, n)
        sign = MathCalculator.pow(M, d, p, q)

        check = MathCalculator.pow(sign, e, p, q)
        assert check == M
