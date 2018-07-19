"""APIs for working with report repositories.
"""

__all__ = ('ReportRepo',)

from pathlib import Path


class ReportRepo:
    """Report repository.

    Parameters
    ----------
    dirname : `pathlib.Path` or `str`
        Path to the report repository directory. This directory is a clone of
        the report's Git repository on the local filesystem.
    """

    def __init__(self, dirname):
        super().__init__()

        # Set and validate dirname
        if not isinstance(dirname, Path):
            dirname = Path(dirname)
        self._dirname = dirname.resolve()
        if not self._dirname.is_dir():
            raise OSError('Report repo not found at {}'.format(self._dirname))

    @property
    def dirname(self):
        """Directory path of the cloned report repository (`pathlib.Path`).
        """
        return self._dirname
