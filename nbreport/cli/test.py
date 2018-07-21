"""Implementation of the nbreport test command.
"""

__all__ = ('test',)

import logging
import pathlib

import click

from ..repo import ReportRepo
from ..instance import ReportInstance


@click.command()
@click.argument(
    'repo_path', default=None, required=True, nargs=1,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
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
@click.pass_context
def test(ctx, repo_path, instance_path, instance_id, overwrite):
    """Test a notebook repository by instantiating and computing it.

    REPO_PATH is the path to the report repository directory.
    """
    logger = logging.getLogger()

    repo_path = pathlib.Path(repo_path)

    if instance_path is None:
        instance_path = pathlib.Path(
            '{0}-{1}'.format(str(repo_path.name), instance_id))
    else:
        instance_path = pathlib.Path(instance_path)

    report_repo = ReportRepo(repo_path)

    instance = ReportInstance.from_report_repo(
        report_repo, instance_path, instance_id, overwrite=overwrite)
    logger.debug('Created instance %s at %s', instance, instance_path)
