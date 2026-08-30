from functools import singledispatch
from typing import Any

@singledispatch
def unlist(x: Any, **kwargs) -> Any:
    """Unlist a structured list-like container into a flat sequence.

    Args:
        x:
            The structured object/container to flatten.
        **kwargs:
            Optional keyword arguments passed to the specific implementation.

    Returns:
        A flat representation of the sequence.
    """
    if hasattr(x, "unlist"):
        return x.unlist(**kwargs)
        
    if isinstance(x, (list, tuple)):
        flat = []
        for item in x:
            if isinstance(item, (list, tuple)):
                flat.extend(unlist(item))
            else:
                flat.append(item)
        return type(x)(flat)
        
    return x
