import hashlib
from .types import StreamTypes
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def hash256(b):
    if type(b) is bytes:
        return hashlib.sha256(hashlib.sha256(b).digest()).digest()
    elif type(b) is str:
        b = bytes(b, "utf-8")
        return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def encode_base58(s: bytes):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break

    num = int.from_bytes(s, "big")
    prefix = "1" * count
    result = ""
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result

    return prefix + result


def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])


def hash160(s):
    """sha256 followed b ripemd160"""
    sha256 = hashlib.sha256(s).digest()
    return hashlib.new("ripemd160", sha256).digest()


def little_endian_to_int(b: bytes) -> int:
    return int.from_bytes(b, "little")


def int_to_little_endian(i: int, length: int) -> bytes:
    return i.to_bytes(length, "little")


def read_varint(s: StreamTypes) -> int:
    """Reads a variable integere from a stream of bytes"""
    i = int.from_bytes(s.read(1))
    if i == 0xfd:
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        return little_endian_to_int(s.read(8))
    else:
        return i


def encode_varint(i: int) -> bytes:
    """Encodes an integer as a varint"""
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b"\xfd" + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b"\xfe" + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b"\xff" + int_to_little_endian(i, 8)
    else:
        raise ValueError(
            f"Integer {i} too large. Must be less than {0x10000000000000000}")
