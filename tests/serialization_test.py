import unittest
from tests.generic_test import GenericTest

from bitcoin import PrivateKey, S256Point, Signature
from bitcoin.utils import encode_base58

class SerializationTest(GenericTest):
    def __init__(self, *args, **kwargs):
        super(SerializationTest, self).__init__(*args, **kwargs)

    def test_base58_encoding(self):
        hex1 = "7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d"
        expected_encoding1 = "9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6"
        encoding1 = encode_base58(bytes.fromhex(hex1))

        self.assertEqual(expected_encoding1, encoding1)

        hex2 = "eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c"
        expected_encoding2 = "4fE3H2E6XMp4SsxtwinF7w9a34ooUrwWe4WsW1458Pd"
        encoding2 = encode_base58(bytes.fromhex(hex2))

        self.assertEqual(expected_encoding2, encoding2)

        hex3 = "c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6"
        expected_encoding3 = "EQJsjkd6JaGwxrjEhfeqPenqHwrBmPQZjJGNSCHBkcF7"
        encoding3 = encode_base58(bytes.fromhex(hex3))

        self.assertEqual(expected_encoding3, encoding3)
        self.logger.info("Base58 Encodigng test passed!")

    # =========== Public Key Serialization ===========

    def test_uncompressed_sec_serialization(self):
        public_key = PrivateKey(secret_key=0xdeadbeef12345).pub_key
        sec = public_key.sec(compressed=False).hex()
        expected_sec = "04d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f842efa762fd59961d0e99803c61edba8b3e3f7dc3a341836f97733aebf987121"
        self.assertEqual(sec, expected_sec)
        self.logger.info("Uncompressed Sec Serialization test passed!")

    def test_compressed_sec_serialization(self):
        public_key = PrivateKey(secret_key=0xdeadbeef12345).pub_key
        sec = public_key.sec().hex()
        expected_sec = "03d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f"
        self.assertEqual(sec, expected_sec)
        self.logger.info("Compressed Sec Serialization test passed!")

    def test_compressed_sec_parsing(self):
        sec = "02027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9d"
        public_key = PrivateKey(secret_key=2018**5).pub_key

        parsed_public_key = S256Point.parse(bytes.fromhex(sec))
        self.assertEqual(public_key, parsed_public_key)

        self.logger.info("Compressed Sec Parsing test passed!")

    def test_uncompressed_sec_parsing(self):
        sec = "04ffe558e388852f0120e46af2d1b370f85854a8eb0841811ece0e3e03d282d57c315dc72890a4f10a1481c031b03b351b0dc79901ca18a00cf009dbdb157a1d10"
        public_key = PrivateKey(secret_key=5000).pub_key

        parsed_public_key = S256Point.parse(bytes.fromhex(sec))
        self.assertEqual(public_key, parsed_public_key)

        self.logger.info("Uncompressed Sec Parsing test passed!")


    # =========== Signature Serialization ===========

    def test_der_serialization(self):
        expected_der = "3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec"
        sig = Signature(
            r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,
            s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        )
        self.assertEqual(expected_der, sig.der().hex())
        self.logger.info("DER Serialization test passed!")

    def test_der_parsing(self):
        der = "3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec"
        sig = Signature.parse(bytes.fromhex(der))
        expected_sig = Signature (
            r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,
            s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        )
        self.assertEqual(expected_sig, sig)
        self.logger.info("DER Parsing test passed!")


    # =========== Private Key Serialization ===========

    def test_wif(self):
        expected_wif1 = "cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK"
        priv1 = PrivateKey(secret_key=5003)
        self.assertEqual(expected_wif1, priv1.wif(compressed=True, testnet=True))

        expected_wif2 = "91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic"
        priv2 = PrivateKey(secret_key=2021**5)
        self.assertEqual(expected_wif2, priv2.wif(compressed=False, testnet=True))

        expected_wif3 = "KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a"
        priv3 = PrivateKey(secret_key=0x54321deadbeef)
        self.assertEqual(expected_wif3, priv3.wif())

        self.logger.info("WIF test passed!")

    # =========== Addresses ===========

    def test_address(self):
        expected_address1 = "mmTPbXQFxboEtNRkwfh6K51jvdtHLxGeMA"
        priv1 = PrivateKey(secret_key=5002)
        self.assertEqual(expected_address1, priv1.address(compressed=False, testnet=True))

        expected_address2 = "mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH"
        priv2 = PrivateKey(secret_key=2020**5)
        self.assertEqual(expected_address2, priv2.address(testnet=True))

        expected_address3 = "1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1"
        priv3 = PrivateKey(secret_key=0x12345deadbeef)
        self.assertEqual(expected_address3, priv3.address())

        self.logger.info("Addresses test passed!")

if __name__ == "__main__":
    unittest.main()