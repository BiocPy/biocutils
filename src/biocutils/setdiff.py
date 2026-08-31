from collections.abc import Sequence

from .is_missing_scalar import is_missing_scalar
from .map_to_index import DUPLICATE_METHOD


from functools import singledispatch

@singledispatch
def _setdiff_internal(first: Sequence, *other: Sequence, duplicate_method: DUPLICATE_METHOD = "first") -> list:
    present = set()
    for i in range(len(other)):
        for f in other[i]:
            if not is_missing_scalar(f):
                present.add(f)

    output = []

    def handler(f):
        if not is_missing_scalar(f) and f not in present:
            output.append(f)
            present.add(f)

    if duplicate_method == "first":
        for f in first:
            handler(f)
    else:
        for f in reversed(first):
            handler(f)
        output.reverse()

    return output

def setdiff(*x: Sequence, duplicate_method: DUPLICATE_METHOD = "first") -> list:
    """Identify the set difference of values in multiple sequences, preserves
    the order of values in the first sequence.
    
    This is a :py:func:`~functools.singledispatch` generic, allowing developers
    to specify custom methods for their own classes.

    Args:
        x:
            One or more sequences of interest containing hashable values.
            Ignores missing values as defined in
            :py:meth:`~biocutils.is_missing_scalar.is_missing_scalar`.

        duplicate_method:
            Whether to keep the first or last occurrence of duplicated values
            when preserving order in the first sequence.

    Returns:
        Difference of values in the first sequence but not in the others.
        If no sequences are provided, an empty list is returned.
        If one sequence is provided, the unique values in the sequence are returned.
    """
    nargs = len(x)
    if nargs == 0:
        return []

    return _setdiff_internal(x[0], *x[1:], duplicate_method=duplicate_method)

setdiff.register = _setdiff_internal.register
