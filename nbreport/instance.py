"""APIs for working with report instances.
"""

__all__ = ('ReportInstance',)

from pathlib import Path
import shutil

from .repo import ReportConfig


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

    @classmethod
    def from_report_repo(self, report_repo, instance_dirname, instance_id,
                         overwrite=False):
        """Create a new instance of a report from a report repository.

        This creates a directory on the file system for the instance.

        Parameters
        ----------
        report_repo : `nbreport.repo.ReportRepo`
            Report repository.
        instance_dirname : `pathlib.Path` or `str`
            Directory path for the new instance.
        instance_id : `str`
            Identifier of the report instance.
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

        return instance
