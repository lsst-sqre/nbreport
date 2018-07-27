"""Implementation of the nbreport test command.
"""

__all__ = ('test',)

import logging
import pathlib
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

import click

from ..compute import compute_notebook_file
from ..repo import ReportRepo
from ..instance import ReportInstance


@click.command()
@click.argument(
    'repo_path_or_url', default=None, required=True, nargs=1,
)
@click.option(
    '-c', '--config', 'template_variables', nargs=2, type=str, multiple=True,
    help='Template key-value pairs. For example, if the report has a template '
         'variable called ``title``, you can provide it as ``-c title "Hello '
         'World!"``. You can provide multiple -c/--config options.'
)
@click.option(
    '-d', '--dir', 'instance_path', type=click.Path(),
    help='Path of the report directory. By default, the report directory '
         'is created in the current working directory and is named '
         '{{handle}}-{{id}}.'
)
@click.option(
    '--id', 'instance_id', type=str, default='test',
    help='Identifier of the instance. By default, this is ``test``.'
)
@click.option(
    '--overwrite/--no-overwrite', default=True,
    help='Whether or not to overwrite an existing test instance. Overwriting '
         'is enabled by default.'
)
@click.option(
    '--timeout', type=int, default=None,
    help='Timeout for computing individual notebook cells. Default is no '
         'timeout.'
)
@click.option(
    '-k', '--kernel', type=str, default='',
    help='Name of the Jupyter kernel to use for computing the notebook. '
         'The default Python kernel is used if this option is not set.'
)
@click.option(
    '--git-subdir', 'git_repo_subdir', type=str, default=None,
    help='If cloning from a Git repository and the report is not at the root '
         'of that Git repository, set Git repo-relative path to the report '
         'with this option.'
)
@click.option(
    '--git-ref', 'git_repo_ref', type=str, default='master',
    help='If cloning from a Git repository, check out a specific Git ref '
         '(branch or tag name).'
)
@click.pass_context
def test(ctx, repo_path_or_url, template_variables, instance_path, instance_id,
         overwrite, timeout, kernel, git_repo_subdir, git_repo_ref):
    """Test a notebook repository by instantiating and computing it, but
    without publishing the result.

    Use ``nbreport test`` when developing notebook repositories.
    The ``nbreport test`` command does the following steps:

    1. Instantiates a report istance from either a local report directory or
       a report on GitHub.

    2. Renders the template variables given defaults and user-provided
       configurations (see the ``-c`` option).

    3. Computes the notebook.

    **Example**

    .. code-block:: bash

        nbreport test https://github.com/lsst-sqre/nbreport \
          --git-subdir tests/TESTR-000 -c title "My first report"

    **Required arguments**

    ``REPO_PATH``
        The path to the report repository directory.
    """
    logger = logging.getLogger()

    template_variables = dict(template_variables)
    logger.debug('Template variables: %s', template_variables)

    if is_url(repo_path_or_url):
        with TemporaryDirectory() as tempdir:
            report_repo = ReportRepo.git_clone(
                repo_path_or_url,
                clone_base_dir=tempdir,
                subdir=git_repo_subdir,
                checkout=git_repo_ref
            )
            _run(report_repo, instance_path, instance_id, template_variables,
                 overwrite, timeout, kernel)
    else:
        report_repo = ReportRepo(repo_path_or_url)
        _run(report_repo, instance_path, instance_id, template_variables,
             overwrite, timeout, kernel)


def _run(report_repo, instance_path, instance_id, template_variables,
         overwrite, timeout, kernel):
    logger = logging.getLogger()

    if instance_path is None:
        instance_path = pathlib.Path(
            '{0}-{1}'.format(str(report_repo.dirname.name), instance_id))
    else:
        instance_path = pathlib.Path(instance_path)

    instance = ReportInstance.from_report_repo(
        report_repo, instance_path, instance_id, overwrite=overwrite,
        context=template_variables)
    logger.debug('Created instance %s at %s', instance, instance_path)

    compute_notebook_file(instance.ipynb_path, timeout=timeout,
                          kernel_name=kernel)
    logger.debug('Computed notebook %s', instance.ipynb_path)


def is_url(path_or_url):
    """Test if the token represents a URL or a local path.
    """
    parts = urlparse(path_or_url)
    if parts.scheme is not '':
        return True
    else:
        return False
