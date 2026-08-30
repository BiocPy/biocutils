import numpy as np
from typing import Any, List, Union

class Rle:
    def __init__(self, values: Any, lengths: Any = None):
        """Initialize Run-Length Encoded vector.

        Args:
            values:
                Sequence of values, or a single value if lengths is specified.
            lengths:
                Sequence of run lengths matching each value, or None if values should be run-length compressed.
        """
        if lengths is None:
            vals = np.asarray(values)
            if len(vals) == 0:
                self.values = np.array([], dtype=vals.dtype)
                self.lengths = np.array([], dtype=np.int32)
            else:
                change_indices = np.where(vals[:-1] != vals[1:])[0]
                runs = np.diff(np.concatenate([[-1], change_indices, [len(vals) - 1]]))
                self.values = np.concatenate([[vals[0]], vals[change_indices + 1]])
                self.lengths = runs.astype(np.int32)
        else:
            self.values = np.asarray(values)
            self.lengths = np.asarray(lengths, dtype=np.int32)

    def __len__(self) -> int:
        return int(np.sum(self.lengths))

    def to_numpy(self) -> np.ndarray:
        """Decompress Rle back to a dense numpy array."""
        return np.repeat(self.values, self.lengths)

    def __getitem__(self, idx: Union[int, slice]) -> Any:
        dense = self.to_numpy()
        return dense[idx]

    def __repr__(self) -> str:
        return f"Rle(values={self.values.tolist()}, lengths={self.lengths.tolist()})"
