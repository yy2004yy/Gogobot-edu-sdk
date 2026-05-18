"""
Top-level import shim for local repository usage.

This allows `import aidog_sdk` to work when running scripts from the
workspace root (where this directory is on `sys.path`).
"""

from .aidog_sdk import *  # noqa: F401,F403
from .aidog_sdk import __all__ as __all__  # re-export public symbols
from .aidog_sdk import __version__ as __version__

