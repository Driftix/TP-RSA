import random
from sympy import isprime
import base64


class KeyManager:
    def __init__(self,params):
        self.params = params

    def generate_keys(self):
        name = self.params.name
        size = self.params.size

        p, q = self.__generate_prime(size), self.__generate_prime(size)
        while p == q:
            q = self.__generate_prime(size)

        n = p * q
        n_prime = (p - 1) * (q - 1)

        e = random.randint(2, n_prime - 1)
        while isprime(e) is False or n_prime % e == 0:
            e = random.randint(2, n_prime - 1)

        d = pow(e, -1, n_prime)

        return (n, e), (n, d)
    def __generate_prime(self, size):
        while True:
            num = random.randint(10**(size-1), 10**size - 1)
            if isprime(num):
                return num

    def generate_keys_b64(self):
        pub_key , priv_key = self.generate_keys()
        n1 , e  = pub_key
        n2 , d = priv_key
        if n1 == n2:
            pub_key_b64 = base64.b64encode(str(hex(n1)[2:] + '\n' + hex(e)[2:]).encode()).decode()
            priv_key_b64 = base64.b64encode(str(hex(n2)[2:] + '\n' + hex(d)[2:]).encode()).decode()
        else :
            raise SystemExit("Mauvais calcul de n")
        return pub_key_b64 , priv_key_b64

class KeyParameters():
    def __init__(self, name, size):
        self.name = name
        self.size = size