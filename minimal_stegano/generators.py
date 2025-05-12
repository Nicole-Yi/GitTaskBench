from typing import Iterator

def identity() -> Iterator[int]:
    """Simple identity generator"""
    n = 0
    while True:
        yield n
        n += 1
