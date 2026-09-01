__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


import importlib.util


def is_package_installed(package_name: str, verbose: bool = False) -> bool:
    """Check if a package is installed.

    Args:
        package_name:
            Package name.

    Returns:
        True if package is installed, otherwise False.
    """
    try:
        _installed = importlib.util.find_spec(package_name) is not None
    except Exception:
        _installed = False

    if not _installed and verbose:
        print(f"Package '{package_name}' is not installed.")

    return _installed
