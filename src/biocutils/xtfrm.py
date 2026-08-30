from functools import singledispatch
from typing import Any

import numpy

from .Factor import Factor


@singledispatch
def xtfrm(x: Any) -> Any:
    """Obtain a numeric representation of the elements of ``x`` that can be sorted.

    Args:
        x:
            Values to be transformed.

    Returns:
        A numeric representation (usually a NumPy array or a sequence of numbers)
        whose elements sort in the same relative order as ``x``.
    """
    if hasattr(x, "__xtfrm__"):
        return x.__xtfrm__()

    if isinstance(x, numpy.ndarray) and numpy.issubdtype(x.dtype, numpy.number):
        return x

    from .order import order
    from .subset import subset

    o = order(x)
    ranks = numpy.empty(len(x), dtype=int)
    if len(x) == 0:
        return ranks

    sorted_x = subset(x, o)
    current_rank = 0
    for i, idx in enumerate(o):
        if i > 0 and sorted_x[i] != sorted_x[i - 1]:
            current_rank += 1
        ranks[idx] = current_rank

    return ranks


@xtfrm.register
def _xtfrm_Factor(x: Factor) -> numpy.ndarray:
    return x.get_codes()
