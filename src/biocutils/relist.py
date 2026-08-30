from typing import Any

_relist_registry = {}

def relist(flesh: Any, skeleton: Any, **kwargs) -> Any:
    """Relist a flat sequence into the structure/shape of a skeleton.

    Args:
        flesh:
            The flat sequence/vector to reshape.
        skeleton:
            The template container whose structure should be replicated.

    Returns:
        A reshaped nested container of the same class/type as skeleton.
    """
    for cls in type(skeleton).__mro__:
        if cls in _relist_registry:
            return _relist_registry[cls](flesh, skeleton, **kwargs)
            
    if hasattr(skeleton, "relist"):
        return skeleton.relist(flesh, **kwargs)
        
    if isinstance(skeleton, (list, tuple)):
        res = []
        curr = 0
        for item in skeleton:
            if isinstance(item, (list, tuple)):
                nested_len = len(item)
                res.append(relist(flesh[curr : curr + nested_len], item))
                curr += nested_len
            else:
                res.append(flesh[curr])
                curr += 1
        return type(skeleton)(res)
        
    raise TypeError(f"No relist implementation found for skeleton type '{type(skeleton).__name__}'")

def register(cls):
    def decorator(func):
        _relist_registry[cls] = func
        return func
    return decorator

relist.register = register
