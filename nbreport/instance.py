"""APIs for working with report instances.
"""

__all__ = ('ReportInstance',)

from pathlib import Path
import shutil


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

    @classmethod
    def from_report_repo(self, report_repo, instance_dirname, overwrite=False):
        """Create a new instance of a report from a report repository.

        This creates a directory on the file system for the instance.

        Parameters
        ----------
        report_repo : `nbreport.repo.ReportRepo`
            Report repository.
        instance_dirname : `pathlib.Path` or `str`
            Directory path for the new instance.
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
        # FIXME replace this file discovery with configuration from the Report
        # instance
        shutil.copy(
            report_repo.context_path,
            instance_dirname / 'cookiecutter.json')
        source_ipynb = next(report_repo.dirname.glob('*.ipynb'))
        dest_ipynb = instance_dirname / source_ipynb.name
        shutil.copy(source_ipynb, dest_ipynb)

        return ReportInstance(instance_dirname)
