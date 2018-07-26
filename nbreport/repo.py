"""APIs for working with report repositories.
"""

__all__ = ('ReportRepo', 'ReportConfig')

from io import StringIO
import os
from pathlib import Path
from urllib.parse import urlparse

import git
import nbformat
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

    @classmethod
    def git_clone(cls, url, clone_base_dir=None, checkout='master',
                  subdir=None):
        """Create a ReportRepo instance by cloning from a Git repository.

        Parameters
        ----------
        url : `str`
            URL of the remote Git repository.
        clone_base_dir : `str`, optional
            Directory to clone the Git repository into. Defaults to the
            current working directory.
        checkout : `str`, optional
            Git ref (branch or tag) to check out. By default, the default
            (``master``) branch is checked out.
        subdir : `str`, optional
            If a report repository is not located in the root of a Git
            repository, set the Git-repo-relative directory path with this
            argument.

        Returns
        -------
        ReportRepo
            Report repository instance (located on a local file system).
        """
        url_parts = urlparse(url)
        repo_name = url_parts.path.split('/')[-1]
        repo_name = os.path.splitext(repo_name)[0]

        if clone_base_dir is None:
            clone_dir = Path(repo_name)
        else:
            clone_dir = Path(clone_base_dir) / repo_name

        git.Repo.clone_from(url, clone_dir, branch=checkout)

        if subdir is None:
            return cls(clone_dir)
        else:
            return cls(clone_dir / subdir)

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

    def open_notebook(self):
        """Open the repository's notebook file.

        Returns
        -------
        notebook : `nbformat.NotebookNode`
            The repository's notebook file as a `~nbformat.NotebookNode`
            instance. If modified, the notebook must be explicitly written
            to disk with `nbformat.write` to be persisted.
        """
        return nbformat.read(str(self.ipynb_path),
                             as_version=nbformat.NO_CONVERT)


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
