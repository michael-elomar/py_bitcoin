from .finite_fields import FieldElement, S256Field
from .utils import encode_base58_checksum, hash160

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

    def hash160(self, compressed=True):
        return hash160(self.sec(compressed=compressed))

    def address(self, compressed=True, testnet=False):
        """
        Returns the address string
        """
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b"\x6f"
        else:
            prefix = b"\x00"
        return encode_base58_checksum(prefix + h160)