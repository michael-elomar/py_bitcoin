from tests.generic_test import GenericTest
from finite_field import FieldElement
import unittest


class FiniteFieldTest(GenericTest):
    def __init__(self, *args, **kwargs):
        super(FiniteFieldTest, self).__init__(*args, **kwargs)

    def test_eq(self):
        a = FieldElement(7, 13)
        b = FieldElement(6, 13)
        self.assertNotEqual(a, b)
        self.assertEqual(a, a)
        self.logger.info("Equality test passed")

    def test_neq(self):
        a = FieldElement(7, 25)
        b = FieldElement(16, 25)
        self.assertNotEqual(a, b)
        self.logger.info("Inequality test passed")

    def test_add(self):
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        c = FieldElement(6, 13)
        self.assertEqual(a + b, c)
        self.logger.info("Addition test passed")

    def test_sub(self):
        a = FieldElement(12, 25)
        b = FieldElement(13, 25)
        c = FieldElement(1, 25)
        d = FieldElement(24, 25)
        self.assertEqual(c, b - a)
        self.assertEqual(d, a - b)
        self.logger.info("Subtraction test passed")

    def test_mul(self):
        a = FieldElement(5, 19)
        b = FieldElement(3, 19)
        ab = FieldElement(15, 19)
        c = FieldElement(8, 19)
        d = FieldElement(17, 19)
        cd = FieldElement(3, 19)

        self.assertEqual(a * b, ab)
        self.assertEqual(c * d, cd)

        self.logger.info("Multiply test passed")

    def test_pow(self):
        a = FieldElement(7, 19)
        a3 = FieldElement(1, 19)
        self.assertEqual(a ** 3, a3)

        b = FieldElement(9, 19)
        b12 = FieldElement(7, 19)
        self.assertEqual(b ** 12, b12)

        self.logger.info("Power test passed")

    def test_negative_pow(self):
        a = FieldElement(7, 19)
        inv_a = a ** (-1)
        inv_a2 = a ** (-2)
        self.assertEqual(a * inv_a, FieldElement(1, 19))

        self.assertEqual(a * inv_a2 * a, FieldElement(1, 19))
        self.logger.info("Negative Power test passed")

    def test_comparison(self):
        a = FieldElement(12, 25)
        b = FieldElement(13, 25)
        other = 12
        self.assertLessEqual(a, b)
        self.assertLess(other, b)
        self.assertGreater(b, other)
        self.logger.info("Comparison test passed")

    def test_true_div(self):
        a = FieldElement(2, 19)
        b = FieldElement(7, 19)
        c = FieldElement(3, 19)
        d = FieldElement(5, 19)
        e = FieldElement(9, 19)
        self.assertEqual(a / b, c)
        self.assertEqual(b / d, e)

        self.logger.info("True division test passed")


if __name__ == '__main__':
    unittest.main()
