import unittest
import hyfed
import numpy as np


class StrongRandomTestCase(unittest.TestCase):

    def setUp(self):
        self.n = 100

    def tearDown(self):
        self.n = None

    def test_randint64(self):
        result = hyfed.rand.randint64(self.n)
        self.assertEqual((self.n, ), result.shape)
        self.assertEqual(np.int64, result.dtype)

    def test_rand(self):
        result = hyfed.rand.rand(0., 1., self.n, dtype=np.float64)
        self.assertEqual((self.n, ), result.shape)
        self.assertEqual(np.float64, result.dtype)

    def test_randn(self):
        result = hyfed.rand.randn(0., 1., self.n, dtype=np.float64)
        self.assertEqual((self.n, ), result.shape)
        self.assertEqual(np.float64, result.dtype)
