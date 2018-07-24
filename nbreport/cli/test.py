"""Implementation of the nbreport test command.
"""

__all__ = ('test',)

import logging
import pathlib

import click

from ..compute import compute_notebook_file
from ..repo import ReportRepo
from ..instance import ReportInstance


@click.command()
@click.argument(
    'repo_path', default=None, required=True, nargs=1,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
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
@click.pass_context
def test(ctx, repo_path, template_variables, instance_path, instance_id,
         overwrite, timeout, kernel):
    """Test a notebook repository by instantiating and computing it.

    REPO_PATH is the path to the report repository directory.
    """
    logger = logging.getLogger()

    template_variables = dict(template_variables)
    logger.debug('Template variables: %s', template_variables)
    print('Template variables: %s' % template_variables)

    repo_path = pathlib.Path(repo_path)

    if instance_path is None:
        instance_path = pathlib.Path(
            '{0}-{1}'.format(str(repo_path.name), instance_id))
    else:
        instance_path = pathlib.Path(instance_path)

    print('instance_path', instance_path)

    report_repo = ReportRepo(repo_path)

    print('report_repo', report_repo)

    instance = ReportInstance.from_report_repo(
        report_repo, instance_path, instance_id, overwrite=overwrite,
        context=template_variables)
    logger.debug('Created instance %s at %s', instance, instance_path)
    print('Created instance %s at %s' % (instance, instance_path))

    compute_notebook_file(instance.ipynb_path, timeout=timeout,
                          kernel_name=kernel)
    logger.debug('Computed notebook %s', instance.ipynb_path)
    print('Computed notebook %s' % instance.ipynb_path)
