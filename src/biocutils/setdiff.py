from collections.abc import Sequence

from .is_missing_scalar import is_missing_scalar
from .map_to_index import DUPLICATE_METHOD


def setdiff(*x: Sequence, duplicate_method: DUPLICATE_METHOD = "first") -> list:
    """Identify the set difference of values in multiple sequences, preserves
    the order of values in the first sequence.

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

    first = x[0]
    present = set()

    for i in range(1, nargs):
        for f in x[i]:
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
