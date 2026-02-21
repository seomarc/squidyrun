"""
Filesystem adapters
"""

from .local_fs import LocalFileSystem
from .mock_fs import MockFileSystem

__all__ = ["LocalFileSystem", "MockFileSystem"]
