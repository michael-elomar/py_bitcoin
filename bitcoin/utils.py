import hashlib

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

def int_to_little_endian(i: int) -> bytes:
    return i.to_bytes(32, "little")

