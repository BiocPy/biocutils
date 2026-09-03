import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .assign import assign
from .assign_rows import assign_rows
from .assign_sequence import assign_sequence
from .biocobject import BiocObject
from .BooleanList import BooleanList
from .combine import combine
from .combine_columns import combine_columns
from .combine_rows import combine_rows
from .combine_sequences import combine_sequences
from .convert_to_dense import convert_to_dense
from .duplicated import duplicated, unique
from .extract_column_names import extract_column_names
from .extract_row_names import extract_row_names
from .Factor import Factor
from .factorize import factorize
from .FloatList import FloatList
from .get_height import get_height
from .IntegerList import IntegerList
from .intersect import intersect
from .is_high_dimensional import is_high_dimensional
from .is_list_of_type import is_list_of_type
from .is_missing_scalar import is_missing_scalar
from .map_to_index import map_to_index
from .match import MatchIndex, create_match_index, match
from .NamedList import NamedList
from .Names import Names
from .normalize_subscript import SubscriptTypes, normalize_subscript
from .order import order, sort
from .print_truncated import print_truncated, print_truncated_dict, print_truncated_list
from .print_wrapped_table import create_floating_names, print_type, print_wrapped_table, truncate_strings
from .relaxed_combine_columns import relaxed_combine_columns
from .relaxed_combine_rows import relaxed_combine_rows
from .setdiff import setdiff
from .show_as_cell import show_as_cell
from .split import split
from .StringList import StringList
from .subset import subset
from .subset_rows import subset_rows
from .subset_sequence import subset_sequence
from .table import table
from .union import union
from .which import which
