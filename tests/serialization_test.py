import unittest
from tests.generic_test import GenericTest

from bitcoin import PrivateKey, S256Point, Signature

class SerializationTest(GenericTest):
    def __init__(self, *args, **kwargs):
        super(SerializationTest, self).__init__(*args, **kwargs)

    # =========== Public Key Serialization ===========

    def test_uncompressed_sec_serialization(self):
        public_key = PrivateKey(secret_key=0xdeadbeef54321).pub_key
        sec = public_key.sec(compressed=False).hex()
        expected_sec = "0496be5b1292f6c856b3c5654e886fc13511462059089cdf9c479623bfcbe7769032555d1b027c25c2828ba96a176d78419cd1236f71558f6187aec09611325eb6"
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
        der = "3045022037203a0610995fd6074999cb9327b87af4c4978db68c06e8e6e81d282047a7c60221008ca12345c1557dbcaec0d03cecca119fc9a75bf8e690da65c041c8e2738cdaec"
        sig = Signature.parse(bytes.fromhex(der))
        expected_sig = Signature (
            r = 0x37203a0610995fd6074999cb9327b87af4c4978db68c06e8e6e81d282047a7c6,
            s = 0x8ca12345c1557dbcaec0d03cecca119fc9a75bf8e690da65c041c8e2738cdaec
        )
        self.assertEqual(expected_sig, sig)
        self.logger.info("DER Parsing test passed!")
if __name__ == "__main__":
    unittest.main()