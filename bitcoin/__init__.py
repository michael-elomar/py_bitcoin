import hashlib
import hmac


class FieldElement(object):
    def __init__(self, num: int, prime: int):
        if num >= prime or num < 0:
            error_msg = f"Num {num} is not in field range 0 to {prime - 1}"
            raise ValueError(error_msg)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f"FieldElement_{self.prime}({self.num})"

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if other is None:
            raise ValueError("Cannot add FieldElement and None")
        if other.prime != self.prime:
            raise ValueError("Cannot add field elements with different primes")
        return self.__class__((self.num + other.num) % self.prime, self.prime)

    def __sub__(self, other):
        if other is None:
            raise ValueError("Cannot subtract FieldElement and None")
        if other.prime != self.prime:
            raise ValueError("Cannot subtract field elements with different primes")
        return self.__class__((self.num - other.num) % self.prime, self.prime)

    def __mul__(self, other):
        if other is None:
            raise ValueError("Cannot multiply FieldElement and None")
        if type(other) is not type(self):
            if type(other) is int:
                return self.__rmul__(other)
        elif other.prime != self.prime:
            raise ValueError("Cannot multiply field elements with different primes")
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
            raise ValueError("Cannot divide field elements with different primes")
        other = other ** (other.prime - 2)
        return self * other

    def __lt__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError("other does not belong to the Field")
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
                raise ValueError("other does not belong to the Field")
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
                raise ValueError("other does not belong to the Field")
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
                raise ValueError("other does not belong to the Field")
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
        return "{:x}".format(self.num).zfill(64)

    def sqrt(self):
        return self ** ((self.P + 1) // 4)

class Point:
    def __init__(
        self,
        x: FieldElement,
        y: FieldElement,
        a: FieldElement,
        b: FieldElement,
        _tol=1e-12
    ):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if self.x is None and self.y is None:
            return
        if self.y ** 2 - (self.x ** 3 + self.a * self.x + self.b) > _tol:
            error_msg = f"Point ({self.x},{self.y}) is not on the elliptic curve"
            error_msg = f"{error_msg} defined by y^2 = x^3 + a*x + b"
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
    """
    S256Point class inherits from Point class.
    It represents the secp256k1 curve.
    """
    A = 0
    B = 7
    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    P = 2 ** 256 - 2 ** 32 - 977

    def __init__(self, x, y, a=None, b=None, _tol=1e-12):
        a, b = S256Field(self.A), S256Field(self.B)
        if type(x) == int:
            super().__init__(S256Field(x), S256Field(y), a, b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

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
        """
        Verify the validity of the given signature
        Given the signature, and the hash of the message being signed,
        Calculate u, v, and then R = uG + vP.
        if R.x == sig.r, then the signature is valid.

        Args:
            z (int): 256bit number
            sig (Signature): an instance of the class Signature.

        Returns:
            bool: a boolean describing the validity of the signature.
        """

        s_inv = pow(sig.s, self.N - 2, self.N)
        u = z * s_inv % self.N
        v = sig.r * s_inv % self.N
        total = u * S256Point.G() + v * self
        return total.x.num == sig.r

    def sec(self, compressed=True):
        """
        Serializes this point on the secp256k1 curve in theSEC format.

        Args:
            compressed (bool): use compressesd SEC if true.

        Returns:
            bytes: serialized secp256k1 according to uncompressed SEC format.
        """
        if compressed:
            if self.y.num % 2 == 0:
                return b"\x02" + self.x.num.to_bytes(32, "big")
            else:
                return b"\x03" + self.x.num.to_bytes(32, "big")
        else:
            return b"\x04" + self.x.num.to_bytes(32, "big") + self.y.num.to_bytes(32, "big")

    @classmethod
    def parse(self, sec_bin):
        """returns a Point object from a SEC binary (not hex)"""
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], "big")
            y = int.from_bytes(sec_bin[33:65], "big")
            return S256Point(x=x, y=y)
        is_even = sec_bin[0] == 2

        # right side of the equation y^2 = x^3 + 7
        x = S256Field(int.from_bytes(sec_bin[1:], "big"))
        alpha = x**3 + S256Field(self.B)

        # solve for left side
        beta = alpha.sqrt()
        if beta.num % 2 == 0:
            even_beta = beta
            odd_beta = S256Field(self.P - beta.num)
        else:
            even_beta = S256Field(self.P - beta.num)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)

class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return f"Signature(r: {self.r}, s: {self.s})"

    def __eq__(self, __value: object) -> bool:
        if type(__value) is not Signature:
            raise TypeError("Cannot compare Signature instance to an object of a different type.")
        return self.r == __value.r and self.s == __value.s


    def der(self) -> bytes:
        rbin = self.r.to_bytes(32, byteorder="big")
        # remove all null bytes at the beginning
        rbin = rbin.lstrip(b"\x00")

        # if rbin has a high bit, add a \x00
        if rbin[0] & 0x80:
            rbin = b"\x00" + rbin
        result = bytes([2, len(rbin)]) + rbin

        # remove all null bytes at the beginning
        sbin = self.s.to_bytes(32, byteorder="big")
        sbin = sbin.lstrip(b"\x00")

        # if sbin has a high bit, add a \x00
        if sbin[0] & 0x80:
            sbin = b"\x00" + sbin
        result += bytes([2, len(sbin)]) + sbin

        return bytes([0x30, len(result)]) + result

    @classmethod
    def parse(self, der_bin: bytes):
        """
        Parses a binary DER serialization of a ECDSA signature.

        Args:
            der_bin (bytes): serialized bytes of the signature

        Returns:
            Signature: instance of the Signature class containing r and s values
        """
        der_bin = der_bin.lstrip(b"\x30")
        length = der_bin[0]
        der_bin = der_bin.lstrip(length.to_bytes(2))

        der_bin = der_bin.lstrip(b"\x02")
        r_length = der_bin[0]
        der_bin = der_bin.lstrip(r_length.to_bytes(2))
        r = der_bin[:r_length]
        der_bin = der_bin.lstrip(r)
        r = r.lstrip(b"\x00")

        der_bin = der_bin.lstrip(b"\x02")
        s_length = der_bin[0]
        der_bin = der_bin.lstrip(s_length.to_bytes(2))
        s = der_bin[:s_length]
        der_bin = der_bin.lstrip(s)
        s = s.lstrip(b"\x00")

        return Signature(
            r = int.from_bytes(r, "big"),
            s = int.from_bytes(s, "big")
        )


class PrivateKey:
    def __init__(self, secret_key=None):
        if secret_key is None:
            secret_key = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        self.secret_key = secret_key

    @property
    def pub_key(self) -> S256Point:
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
        """
        Deterministic k such that the value of k is unique to the private key
        and the message being signed to make sure the same value of k is never used twice
        for the same private key. If the same k is used twice to sign different messages,
        then the private key can easily be extracted.
        """
        k = b"\x00" * 32
        v = b"\x01" * 32
        if z > S256Point.N:
            z -= S256Point.N
        z_bytes = z.to_bytes(32, "big")
        secret_bytes = self.secret_key.to_bytes(32, "big")
        s256 = hashlib.sha256()
        k = hmac.new(k, v + b"\x00" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b"\x01" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, "big")
            if 1 <= candidate < S256Point.N:
                return candidate
            k = hmac.new(k, v + b"\x00", s256).digest()
            v = hmac.new(k, v, s256).digest()
