from typing import Any
import numpy as np

def pmin(*x: Any, **kwargs) -> Any:
    """Calculate the parallel element-wise minimum of multiple sequences.

    Args:
        *x:
            Sequence objects or vectors of equal length.

    Returns:
        The element-wise minimum.
    """
    if not x:
        raise ValueError("Must specify at least one sequence/vector.")
    
    arrays = [np.asarray(item) for item in x]
    res = arrays[0]
    for arr in arrays[1:]:
        res = np.minimum(res, arr)
    
    if isinstance(x[0], (list, tuple)):
        return type(x[0])(res.tolist())
    return res

def pmax(*x: Any, **kwargs) -> Any:
    """Calculate the parallel element-wise maximum of multiple sequences.

    Args:
        *x:
            Sequence objects or vectors of equal length.

    Returns:
        The element-wise maximum.
    """
    if not x:
        raise ValueError("Must specify at least one sequence/vector.")
        
    arrays = [np.asarray(item) for item in x]
    res = arrays[0]
    for arr in arrays[1:]:
        res = np.maximum(res, arr)
        
    if isinstance(x[0], (list, tuple)):
        return type(x[0])(res.tolist())
    return res
