import secrets
import sys

import numpy as np


STRONG_SECRET = secrets.SystemRandom()
INT64_MAX = sys.maxsize
INT64_MIN = -sys.maxsize - 1


def randint64(n: int):
    """generate random 64-bit integers"""
    x = [STRONG_SECRET.randint(INT64_MIN, INT64_MAX) for _ in range(n)]
    return np.array(x)

def rand(a: float = 0., b: float = 1., n: int = 1, dtype=np.float32):
    x = [STRONG_SECRET.uniform(dtype(a), dtype(b)) for _ in range(n)]
    return np.array(x)

def randn(mu: float = 0., sigma: float = 1., n: int = 1, dtype=np.float32):
    x = [STRONG_SECRET.gauss(dtype(mu), dtype(sigma)) for _ in range(n)]
    return np.array(x)
