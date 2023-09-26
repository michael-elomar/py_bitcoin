import hashlib
import hmac
from bitcoin.utils import hash256


class FieldElement(object):
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error_msg = f"Num {num} is not in field range 0 to {prime - 1}"
            raise ValueError(error_msg)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f'FieldElement_{self.prime}({self.num})'

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if other is None:
            raise ValueError('Cannot add FieldElement and None')
        if other.prime != self.prime:
            raise ValueError('Cannot add field elements with different primes')
        return self.__class__((self.num + other.num) % self.prime, self.prime)

    def __sub__(self, other):
        if other is None:
            raise ValueError('Cannot subtract FieldElement and None')
        if other.prime != self.prime:
            raise ValueError('Cannot subtract field elements with different primes')
        return self.__class__((self.num - other.num) % self.prime, self.prime)

    def __mul__(self, other):
        if other is None:
            raise ValueError("Cannot multiply FieldElement and None")
        if type(other) is not type(self):
            if type(other) is int:
                return self.__rmul__(other)
        elif other.prime != self.prime:
            raise ValueError('Cannot multiply field elements with different primes')
        return self.__class__((self.num * other.num) % self.prime, self.prime)

    def __pow__(self, power, modulo=None):
        if type(power) is not int and type(power) is not float:
            print(type(power))
            raise ValueError(f"power {power} must be a numerical value")
        if power < 0:
            power = power % (self.prime - 1)
        return self.__class__(pow(self.num, power, self.prime), self.prime)

    def __truediv__(self, other):
        if other is None:
            raise ValueError("Cannot divide by a None")
        if other.prime != self.prime:
            raise ValueError('Cannot divide field elements with different primes')
        other = other ** (other.prime - 2)
        return self * other

    def __lt__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError('other does not belong to the Field')
            return self.num < other
        elif type(other) is FieldElement:
            if self.prime != other.prime:
                raise ValueError("Cannot compare two elements of different finite field")
            return self.num < other.num
        else:
            raise TypeError("Cannot compare non numerical types")

    def __gt__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError('other does not belong to the Field')
            return self.num > other
        elif type(other) is FieldElement:
            if self.prime != other.prime:
                raise ValueError("Cannot compare two elements of different finite field")
            return self.num > other.num
        else:
            raise TypeError("Cannot compare non numerical types")

    def __ge__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError('other does not belong to the Field')
            return self.num >= other
        elif type(other) is FieldElement:
            if self.prime != other.prime:
                raise ValueError("Cannot compare two elements of different finite field")
            return self.num >= other.num
        else:
            raise TypeError("Cannot compare non numerical types")

    def __le__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError('other does not belong to the Field')
            return self.num <= other
        elif type(other) is FieldElement:
            if self.prime != other.prime:
                raise ValueError("Cannot compare two elements of different finite field")
            return self.num <= other.num
        else:
            raise TypeError("Cannot compare non numerical types")

    def __rmul__(self, other):
        if type(other) is not int and type(other) is not float:
            raise ValueError(f"{other} must be a numerical type")
        return self.__class__((self.num * other) % self.prime, self.prime)


class S256Field(FieldElement):
    P = 2 ** 256 - 2 ** 32 - 977

    def __init__(self, num, prime=None):
        super().__init__(num, prime=self.P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)


class Point:
    def __init__(self, x, y, a, b, _tol=1e-12):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if self.x is None and self.y is None:
            return
        if self.y ** 2 - (self.x ** 3 + self.a * self.x + self.b) > _tol:
            error_msg = f'Point ({self.x},{self.y}) is not on the elliptic curve'
            error_msg = f'{error_msg} defined by y^2 = x^3 + a*x + b'
            raise ValueError(error_msg)

    @property
    def is_infinity(self):
        return self.x is None and self.y is None

    def _is_on_curve(self, a, b, _tol=1e-12):
        return self.y ** 2 - (self.x ** 3 + a * self.x + b) <= _tol

    def __repr__(self):
        return f"Point_[{self.a.num},{self.b.num}]({self.x}, {self.y})"

    def _same_curve(self, other):
        return self.a == other.a and self.b == other.b

    def __eq__(self, other):
        assert type(other) == Point
        return self.a == other.a and self.b == other.b \
               and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if type(other) is not self.__class__:
            raise TypeError(f"{other} is of type : {type(other)} and  not {self.__class__}")
        if not self._same_curve(other):
            raise TypeError(f"Points {self}, {other} are not on the same curve")
        if self.x is None:
            return other
        if other.x is None:
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x3 = s ** 2 - self.x - other.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)
        if self.x == other.x and self.y == other.y:
            s = (3 * self.x ** 2 + self.a) / (2 * self.y)
            x3 = s ** 2 - 2 * self.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)
        if self == other and self.y == 0:
            return self.__class__(None, None, self.a, self.b)

    def __mul__(self, other):
        return self.__rmul__(other)

    def __rmul__(self, other):
        if type(other) is not int:
            raise ValueError("Scalar coefficient must be an integer")
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while other:
            if other & 1:
                result += current
            current += current
            other >>= 1
        return result


class S256Point(Point):
    A = 0
    B = 7
    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

    def __init__(self, x, y, a=None, b=None, _tol=1e-12):
        a, b = S256Field(self.A), S256Field(self.B)
        if type(x) == int:
            super().__init__(S256Field(x), S256Field(y), a, b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    @staticmethod
    def G():
        return S256Point(
            0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
            0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        )

    def __rmul__(self, other):
        other = other % self.N
        return super().__rmul__(other)

    def __mul__(self, other):
        return self.__mul__(other)

    def verify(self, z, sig):
        s_inv = pow(sig.s, self.N - 2, self.N)
        u = z * s_inv % self.N
        v = sig.r * s_inv % self.N
        total = u * S256Point.G() + v * self
        return total.x.num == sig.r


class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return f"Signature(r: {self.r}, s: {self.s})"


class PrivateKey:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key

    def pub_key(self):
        return self.secret_key * S256Point.G()

    def sign(self, z):
        k = self.deterministic_k(z)
        r = (k * S256Point.G()).x.num
        k_inv = pow(k, S256Point.N - 2, S256Point.N)
        s = (z + r * self.secret_key) * k_inv % S256Point.N
        if s > S256Point.N / 2:
            s = S256Point.N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > S256Point.N:
            z -= S256Point.N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret_key.to_bytes(32, 'big')
        s256 = hashlib.sha256()
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if 1 <= candidate < S256Point.N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()
