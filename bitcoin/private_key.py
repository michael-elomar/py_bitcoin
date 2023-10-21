from .secp256k1 import S256Point
from .utils import encode_base58_checksum
import hmac
import hashlib

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
        result = bytes([0x02, len(rbin)]) + rbin

        # remove all null bytes at the beginning
        sbin = self.s.to_bytes(32, byteorder="big")
        sbin = sbin.lstrip(b"\x00")

        # if sbin has a high bit, add a \x00
        if sbin[0] & 0x80:
            sbin = b"\x00" + sbin
        result += bytes([0x02, len(sbin)]) + sbin

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
        der_bin = der_bin.lstrip(length.to_bytes(2, byteorder="little"))

        der_bin = der_bin.lstrip(b"\x02")
        r_length = der_bin[0]
        der_bin = der_bin.lstrip(r_length.to_bytes(2, byteorder="big"))
        r = der_bin[:r_length]
        der_bin = der_bin.lstrip(r)
        r = r.lstrip(b"\x00")

        der_bin = der_bin.lstrip(b"\x02")
        s_length = der_bin[0]
        der_bin = der_bin.lstrip(s_length.to_bytes(2, byteorder="big"))
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

    def address(self, compressed=True, testnet=False):
        return self.pub_key.address(compressed=compressed, testnet=testnet)

    def wif(self, compressed=True, testnet=False):
        if testnet:
            prefix = b"\xef"
        else:
            prefix = b"\x80"
        secret_bytes = self.secret_key.to_bytes(length=32, byteorder="big")
        if compressed:
            suffix = b"\x01"
        else:
            suffix = b""
        return encode_base58_checksum(prefix + secret_bytes + suffix)