from tests.generic_test import GenericTest
from elliptic_curves import Point
from finite_field import FieldElement
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
        self.logger.info('Point test passed !')


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
        self.logger.info("On Curve Test Passed")

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

        self.logger.info("Not on curve test passed")

    def test_elliptic_curve_addition(self):
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
        self.logger.info("test_elliptic_curve_addition passed")


if __name__ == '__main__':
    unittest.main()
