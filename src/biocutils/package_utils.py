__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def is_package_installed(package_name: str, verbose: bool = False) -> bool:
    """Check if a package is installed.

    Args:
        package_name:
            Package name.

    Returns:
        True if package is installed, otherwise False.
    """
    _installed = False
    try:
        exec(f"import {package_name}")
        _installed = True
    except Exception:
        if verbose:
            print(f"Package '{package_name}' is not installed.")

    return _installed
