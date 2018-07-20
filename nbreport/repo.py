"""APIs for working with report repositories.
"""

__all__ = ('ReportRepo', 'ReportConfig')

from io import StringIO
from pathlib import Path

from ruamel.yaml import YAML


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

    @property
    def context_path(self):
        """Path to the cookiecutter.json template context file
        (`pathlib.Path`).
        """
        return self.dirname / 'cookiecutter.json'

    @property
    def config_path(self):
        """Path to the ``nbreport.yaml`` configuration file (`pathlib.Path`).
        """
        return self.dirname / 'nbreport.yaml'

    @property
    def ipynb_path(self):
        """Path to report's notebook template (`pathlib.Path`).
        """
        return self.dirname / self.config['ipynb']

    @property
    def config(self):
        """Notebook repository configuration (``ReportConfig``).
        """
        return ReportConfig(self.config_path)


class ReportConfig:
    """Configuration for a report repository or instance (the
    ``nbreport.yaml`` file).

    Parameters
    ----------
    path : `pathlib.Path` or `str`
        Path to the ``nbreport.yaml`` configuration file.
    data : `dict`, optional
        Initial data to insert into the configuration.
    """

    def __init__(self, path, data=None):
        super().__init__()

        if not isinstance(path, Path):
            path = Path(path)
        self._path = path

        # This "unsafe" YAML support round-trip preservation of comments
        self._yaml = YAML()

        # Insert initial data
        if data:
            self.update(data)

    def _read(self):
        try:
            with open(self._path) as fp:
                data = self._yaml.load(fp)
        except OSError:
            data = {}
        return data

    def _write(self, data):
        self._yaml.dump(data, self._path)

    def __str__(self):
        data = self._read()
        fp = StringIO()
        self._yaml.dump(data, fp)
        return fp.getvalue()

    def __repr__(self):
        return "{0}('{1!s}')".format(self.__class__.__name__, self._path)

    def __getitem__(self, key):
        """Read a key from the configuration file.

        Parameters
        ----------
        key : `str`
            Key at the top-level of the configuration file.

        Returns
        -------
        obj
            Value of ``key``.
        """
        data = self._read()
        return data[key]

    def __setitem__(self, key, value):
        """Set the value of a key in the configuration file.

        Parameters
        ----------
        key : `str`
            Key.
        value : obj
            Value.
        """
        data = self._read()
        data[key] = value
        self._write(data)

    def keys(self):
        """Get the sequence of keys at the top-level of the configuration file.

        Returns
        -------
        sequence of `str`
            Sequence of keys.
        """
        data = self._read()
        return data.keys()

    def items(self):
        """Iterate over key-value pairs in the configuration file.

        Yields
        ------
        key : `str`
            Key.
        value : obj
            Value
        """
        data = self._read()
        return data.items()

    def update(self, configs):
        """Update a configuration with the given key-value pairs.

        Parameters
        ----------
        configs : `dict`
            Dictionary with configuration key-value pairs.

        Notes
        -----
        Only those keys that are provided will be updated. New keys can also
        be inserted this way.
        """
        data = self._read()
        data.update(configs)
        self._write(data)
