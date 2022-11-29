from generic_test import GenericTest
from elliptic_curves import Point
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
        self.assertEqual(p1+p2, p3)
        self.assertEqual(p2+p2, p4)
        self.logger.info('Point test passed !')


if __name__ == '__main__':
    unittest.main()
