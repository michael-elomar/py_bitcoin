from tests.generic_test import GenericTest
from bitcoin import Point, FieldElement, S256Point, Signature

import unittest


class PointTest(GenericTest):
    def __init__(self, *args, **kwargs):
        super(PointTest, self).__init__(*args, **kwargs)

    def test_point(self):
        p1 = Point(2, 5, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        p3 = Point(3, -7, 5, 7)
        p4 = Point(18.0, 77.0, 5, 7)

        self.assertEqual(p1, p1)
        self.assertNotEqual(p1, p2)
        self.assertEqual(p1 + p2, p3)
        self.assertEqual(p2 + p2, p4)
        self.logger.info('Point test passed!')


class FiniteFieldPointTest(GenericTest):
    def __int__(self, *args, **kwargs):
        super(FiniteFieldPointTest, self).__init__(*args, **kwargs)

    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        points = (
            (192, 105),
            (17, 56),
            (1, 193)
        )
        for x, y in points:
            x = FieldElement(x, prime)
            y = FieldElement(y, prime)
            p = Point(x, y, a, b)
            self.assertTrue(p._is_on_curve(a, b))
        self.logger.info("On Curve Test Passed!")

    def test_not_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        points = (
            (200, 119),
            (42, 99)
        )
        for x, y in points:
            x = FieldElement(x, prime)
            y = FieldElement(y, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

        self.logger.info("Not on curve test passed!")

    def test_add(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)

        x1 = FieldElement(192, 223)
        y1 = FieldElement(105, 223)

        x2 = FieldElement(num=17, prime=223)
        y2 = FieldElement(num=56, prime=223)

        x3 = FieldElement(170, 223)
        y3 = FieldElement(142, 223)

        p1 = Point(x1, y1, a, b)
        p2 = Point(x2, y2, a, b)
        p3 = Point(x3, y3, a, b)

        self.assertEqual(p1 + p2, p3)

        x1 = FieldElement(170, 223)
        y1 = FieldElement(142, 223)

        x2 = FieldElement(num=60, prime=223)
        y2 = FieldElement(num=139, prime=223)

        x3 = FieldElement(220, 223)
        y3 = FieldElement(181, 223)

        p1 = Point(x1, y1, a, b)
        p2 = Point(x2, y2, a, b)
        p3 = Point(x3, y3, a, b)
        self.assertEqual(p1 + p2, p3)
        self.logger.info("Elliptic curve addition test passed!")

    def test_valid_signature(self):
        P = S256Point(
            x=0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c,
            y=0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34
        )
        z1 = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
        sig1 = Signature(
            r=0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395,
            s=0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
        )
        self.assertTrue(P.verify(z1, sig1))

        z2 = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        sig2 = Signature(
            r = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c,
            s = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
        )
        self.assertTrue(P.verify(z2, sig2))


        self.logger.info("Signature verification test passed!")

if __name__ == '__main__':
    unittest.main()
