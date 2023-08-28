import secrets

import numpy as np


def randint64(n: int):
    """generate random 64-bit integers"""
    bytes = secrets.token_bytes(8 * n)
    return np.frombuffer(bytes, dtype=np.int64, count=n)


def rand64(n: int):
    """generate random 64-bit floats"""
    bytes = secrets.token_bytes(8 * n)
    return np.frombuffer(bytes, dtype=np.float64, count=n)
