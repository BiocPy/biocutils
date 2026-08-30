from functools import singledispatch
from typing import Any

@singledispatch
def mcols(x: Any) -> Any:
    """Retrieve metadata columns from an object.

    Args:
        x:
            The object to retrieve mcols from.

    Returns:
        The metadata columns (usually a BiocFrame or None).
    """
    if hasattr(x, "mcols"):
        val = x.mcols
        if callable(val):
            return val()
        return val
    return None

@singledispatch
def set_mcols(x: Any, value: Any) -> Any:
    """Set or replace metadata columns on an object.

    Args:
        x:
            The target object.
        value:
            The new metadata columns.

    Returns:
        A modified object.
    """
    if hasattr(x, "set_mcols"):
        return x.set_mcols(value)
    if hasattr(x, "mcols"):
        try:
            x.mcols = value
            return x
        except AttributeError:
            pass
    raise TypeError(f"Cannot set mcols on type '{type(x).__name__}'")

@singledispatch
def metadata(x: Any) -> Any:
    """Retrieve general metadata from an object.

    Args:
        x:
            The object to retrieve metadata from.

    Returns:
        A dictionary or NamedList containing metadata.
    """
    if hasattr(x, "metadata"):
        val = x.metadata
        if callable(val):
            return val()
        return val
    return None

@singledispatch
def set_metadata(x: Any, value: Any) -> Any:
    """Set or replace general metadata on an object.

    Args:
        x:
            The target object.
        value:
            The new metadata.

    Returns:
        A modified object.
    """
    if hasattr(x, "set_metadata"):
        return x.set_metadata(value)
    if hasattr(x, "metadata"):
        try:
            x.metadata = value
            return x
        except AttributeError:
            pass
    raise TypeError(f"Cannot set metadata on type '{type(x).__name__}'")
