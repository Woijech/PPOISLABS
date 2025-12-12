from __future__ import annotations
import itertools


_counter = itertools.count(1)


def next_id(prefix: str) -> str:
    return f"{prefix}{next(_counter)}"
