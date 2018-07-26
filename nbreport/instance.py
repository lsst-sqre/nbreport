"""APIs for working with report instances.
"""

__all__ = ('ReportInstance',)

from pathlib import Path
import shutil

import nbformat

from .repo import ReportConfig
from .templating import render_notebook, load_template_environment


class ReportInstance:
    """Instance of a notebook-based report.

    Parameters
    ----------
    dirname : `pathlib.Path` or `str`
        Path to the report instance directory.
    """

    def __init__(self, dirname):
        super().__init__()

        # Set and validate dirname
        if not isinstance(dirname, Path):
            dirname = Path(dirname)
        self._dirname = dirname.resolve()
        if not self._dirname.is_dir():
            raise OSError(
                'Report instance not found at {}'.format(self._dirname))

    @property
    def dirname(self):
        """Directory path of the report instance (`pathlib.Path`).
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
        """Path to notebook file (`pathlib.Path`).
        """
        return self.dirname / self.config['ipynb']

    @property
    def config(self):
        """Report instance configuration (``ReportConfig``).
        """
        return ReportConfig(self.config_path)

    def open_notebook(self):
        """Open the instance's notebook file.

        Returns
        -------
        notebook : `nbformat.NotebookNode`
            The repository's notebook file as a `~nbformat.NotebookNode`
            instance. If modified, the notebook must be explicitly written
            to disk with `nbformat.write` to be persisted.
        """
        return nbformat.read(str(self.ipynb_path),
                             as_version=nbformat.NO_CONVERT)

    @classmethod
    def from_report_repo(self, report_repo, instance_dirname, instance_id,
                         context=None, overwrite=False):
        """Create a new instance of a report from a report repository.

        This creates the instance directory on the filesystem and renders
        the templated notebook from a combination of provided context
        variables and defaults.

        Parameters
        ----------
        report_repo : `nbreport.repo.ReportRepo`
            Report repository.
        instance_dirname : `pathlib.Path` or `str`
            Directory path for the new instance.
        instance_id : `str`
            Identifier of the report instance.
        context : `dict`, optional
            Key-value pairs that override the default template context in
            the context file (``cookiecutter.json`,
            `ReportInstance.context_path`).
        overwrite : `bool`, optional
            If `True`, an existing report instance directory will be deleted
            and replaced by the new report instance directory. Default is
            `False`.

        Returns
        -------
        `ReportInstance`
            New instance of a report.
        """
        if not isinstance(instance_dirname, Path):
            instance_dirname = Path(instance_dirname)

        if instance_dirname.exists():
            if overwrite:
                shutil.rmtree(instance_dirname)
            else:
                raise OSError(
                    'Directory already exists: {}'.format(instance_dirname))

        instance_dirname.mkdir()

        # Copy files into the instance
        repo_paths = [
            report_repo.context_path,
            report_repo.ipynb_path,
            report_repo.config_path
        ]
        for source_path in repo_paths:
            shutil.copy(source_path, instance_dirname / source_path.name)

        instance = ReportInstance(instance_dirname)
        instance.config['instance_id'] = instance_id
        instance.config['instance_handle'] = '{handle}-{instance_id}'.format(
            **instance.config)

        instance._render(context=context)

        return instance

    def _render(self, context=None):
        """Render the notebook from the template in the notebook

        Parameters
        ----------
        context : `dict`
            Key-value pairs that override the default template context in
            the context file (``cookiecutter.json`,
            `ReportInstance.context_path`).

        Notes
        -----
        The notebook is rendered and saved in place. A rendered notebook
        cannot be re-rendered.
        """
        notebook = self.open_notebook()

        context, jinja_env = load_template_environment(
            context_path=self.context_path,
            extra_context=context)

        notebook = render_notebook(notebook, context, jinja_env)

        nbformat.write(notebook, str(self.ipynb_path))
