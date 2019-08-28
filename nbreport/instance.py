"""APIs for working with report instances.
"""

__all__ = ('ReportInstance',)

import logging
from pathlib import Path
import shutil
from urllib.parse import urljoin

import nbformat
import requests

from .repo import ReportConfig
from .templating import render_notebook, load_template_environment


class ReportInstance:
    """Instance of a notebook-based report.

    Parameters
    ----------
    dirname : `pathlib.Path` or `str`
        Path to the report instance directory.
    """

    _logger = logging.getLogger(__name__)

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
                         context=None, overwrite=False,
                         published_instance_url=None, ltd_edition_url=None):
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
            `ReportInstance.context_path`). If `None` the notebook *is not*
            rendered. If an empty dict, ``{}``, then the notebook is rendered
            entirely with the default context.
        overwrite : `bool`, optional
            If `True`, an existing report instance directory will be deleted
            and replaced by the new report instance directory. Default is
            `False`.
        published_instance_url : `str`, optional
            URL where the instance is published on LSST the Docs.
        ltd_edition_url : `str`, optional
            URL of the instance's edition resource in the LSST the Docs API.

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
        repo_paths.extend(report_repo.asset_paths)
        for source_path in repo_paths:
            if not source_path.exists():
                self._logger.warning(
                    'Configured asset %s does not exist (skipping)',
                    source_path)
                continue
            dest_path = instance_dirname \
                / source_path.relative_to(report_repo.dirname)
            if not dest_path.parent.is_dir():
                dest_path.parent.mkdir(parents=True)
            shutil.copy(source_path, dest_path)

        instance = ReportInstance(instance_dirname)
        instance.config['instance_id'] = instance_id
        instance.config['instance_handle'] = '{handle}-{instance_id}'.format(
            **instance.config)
        instance.config['published_instance_url'] = published_instance_url
        instance.config['ltd_edition_url'] = ltd_edition_url

        if context is not None:
            instance.render(context=context)

        return instance

    def render(self, context=None):
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

        # Add some notebook metadata to the template context as "system"
        # as opposed to the extra_context that comes from cookiecutter.json
        system_context = {}
        config_data = dict(self.config)  # optimization for bulk reading
        copy_keys = ['handle', 'title', 'git_repo', 'git_repo_subdir',
                     'instance_id', 'instance_handle']
        for key in copy_keys:
            try:
                system_context[key] = config_data[key]
            except KeyError:
                msg = ('Missing nbreport.yaml config key %r; can\'t add it '
                       'to the template context.')
                self._logger.warning(msg)

        context, jinja_env = load_template_environment(
            context_path=self.context_path,
            extra_context=context,
            system_context=system_context)

        # Add the cookiecutter context to the config
        self.config.update({'cookiecutter': context['cookiecutter']})

        notebook = render_notebook(notebook, context, jinja_env)

        # Add config to the notebook metadata
        # Need to remove ruamel.yaml's special typing to be JSON-serializable
        config_dict = dict(self.config)
        config_dict['cookiecutter'] = dict(config_dict['cookiecutter'])
        notebook.metadata.update({'nbreport': config_dict})

        nbformat.write(notebook, str(self.ipynb_path))

    def upload(self, *, github_username, github_token, server):
        """Upload the notebook to the api.lsst.codes/nbreport service
        for publication.

        Parameters
        ----------
        github_username : `str`
            User's GitHub username.
        github_token : `str`
            User's GitHub personal access token, for authentication with
            the api.lsst.codes/nbreport service. ``nbreport login`` can obtain
            this token.
        server : `str`
            URL of the nbreport API server.

        Returns
        -------
        queue_url : `str`
            URL to the nbreport API where you can obtain the status of a
            report instance upload and publication.
        """
        url = urljoin(
            server,
            'nbreport/reports/{product}/instances/{instance}/notebook'.format(
                product=self.config['ltd_product'],
                instance=self.config['instance_id']))

        headers = {
            'Content-Type': 'application/x-ipynb+json'
        }

        with open(self.ipynb_path, 'rb') as fp:
            nb_data = fp.read()

        response = requests.post(
            url,
            headers=headers,
            data=nb_data,
            auth=(github_username, github_token)
        )
        response.raise_for_status()

        data = response.json()
        return data['queue_url']
