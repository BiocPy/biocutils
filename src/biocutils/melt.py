from functools import singledispatch
from typing import Any

import pandas as pd


@singledispatch
def melt(x: Any, **kwargs) -> pd.DataFrame:
    """Melt a container into a tidy long-format pandas DataFrame.

    Args:
        x:
            The object/container to melt.
        **kwargs:
            Optional keyword arguments passed to the specific implementation.

    Returns:
        A pandas DataFrame in long format.
    """
    if hasattr(x, "melt"):
        return x.melt(**kwargs)

    if hasattr(x, "to_pandas"):
        df = x.to_pandas()
        return df.melt(**kwargs)

    raise TypeError(f"No melt implementation found for class '{type(x).__name__}'")
