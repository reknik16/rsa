import random


class MathCalculator:
    @staticmethod
    def __binary_pow(number, degree, module):
        """
        Функция бинарного возведения в степень
        """
        result = 1
        while degree != 0:
            if degree % 2 == 1:
                result = (result * number) % module

            number = (number * number) % module
            degree //= 2

        return result

    @classmethod
    def pow(cls, number, degree, mod1, mod2):
        """
        Бинарное возвезведение в степень с оптимизацией, основанной на китайской теореме об остатках

        result1 - результат по модулю mod1
        result2 - результат по модулю mod2
        result - результат по модулю mod = mod1 * mod2
        """

        result1 = cls.__binary_pow(number, degree % (mod1 - 1), mod1)
        result2 = cls.__binary_pow(number, degree % (mod2 - 1), mod2)
        result = (((result1 - result2) * cls.__binary_pow(mod2, mod1 - 2, mod1)) % mod1) * mod2 + result2
        return result

    @staticmethod
    def euclid(a, b):
        """
        Нахождение НОД с использованием алгоритма Евклида
        """
        while a != 0:
            t = a
            a = b % a
            b = t
        return b

    @staticmethod
    def extended_euclid(a, b):
        """
        Расширенный алгоритм Евклида для нахождения НОД(a, b)
        нахождения обратного элемента в мультипликативной группе
        """
        x = 1
        y = 0
        _x = 0
        _y = 1
        while b != 0:
            q = a // b
            t = b
            b = a % b
            a = t
            t = _x
            _x = x - q * _x
            x = t
            t = _y
            _y = y - q * _y
            y = t
        return a, x, y


class PrimeGenerator:
    __primes = []

    def __init__(self, upper_border):
        self.__calculate_primes(upper_border)

    def __calculate_primes(self, upper_border):
        """
        Решето Эратосфена для нахождения всех простых чисел до upper_border
        """
        is_prime = [True for _ in range(0, upper_border)]
        for i in range(2, upper_border):
            if i * i > upper_border:
                break
            if not is_prime[i]:
                continue
            for j in range(i * i, upper_border, i):
                is_prime[j] = False
        for i in range(2, upper_border):
            if is_prime[i]:
                self.__primes.append(i)

    def is_prime(self, num):
        """
        Проверка числа на простоту
        """
        for j in range(0, len(self.__primes)):
            if num % self.__primes[j] == 0:
                if num == self.__primes[j]:
                    return True
                else:
                    return False

        r = 30
        return self.__rabin_miller(num, r)

    def generate_prime(self, number):
        """
        Генерация случайного простого числа
        """

        result = 2 * random.randrange(2, number // 2 + 1) - 1
        while not self.is_prime(result):
            result = 2 * random.randrange(2, number // 2 + 1) - 1
        return result

    def get_prime_by_number(self, number):
        if len(self.__primes) < number:
            raise IndexError()
        return self.__primes[number]

    @staticmethod
    def __rabin_miller(n, r):
        """
        Тест Рабина-Миллера для проверки числа n на простоту
        """
        b = n - 1
        binary_view = []
        k = 0
        binary_view.append(b % 2)
        b = b // 2
        while b > 0:
            k += 1
            binary_view.append(b % 2)
            b = b // 2

        for _ in range(1, r + 1):
            a = random.randrange(2, n)
            if MathCalculator.euclid(a, n) > 1:
                return False
            d = 1
            for i in range(k, -1, -1):
                x = d
                d = (d * d) % n
                if d == 1 and x != 1 and x != n - 1:
                    return False
                if binary_view[i] == 1:
                    d = (d * a) % n
            if d != 1:
                return False
        return True


class RSA:
    def __init__(self, prime_generator: PrimeGenerator = PrimeGenerator(1000000)):
        self.prime_generator = prime_generator

    def generate_key_rsa(self, n):
        while True:
            p = self.prime_generator.generate_prime(n)
            q = self.prime_generator.generate_prime(n)
            if p != q:
                break
        f = (p - 1)*(q - 1)
        e = 1
        while True:
            e += 2
            (t, x, y) = MathCalculator.extended_euclid(e, f)
            if t <= 1:
                break
        n = p * q
        d = x % f
        return e, d, n, p, q
