"""Implementation for the ``nbreport compute`` command.
"""

__all__ = ('compute',)

import click

from ..compute import compute_notebook_file
from ..instance import ReportInstance


@click.command()
@click.argument(
    'instance_path', default=None, required=True, nargs=1,
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
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
def compute(ctx, instance_path, timeout, kernel):
    """Compute the notebook in a report instance.

    **Required arguments**

    ``INSTANCE_PATH``
        The path to the report repository directory. You can create an
        instance with the ``nbreport init`` command.
    """
    instance = ReportInstance(instance_path)
    compute_notebook_file(instance.ipynb_path, timeout=timeout,
                          kernel_name=kernel)
    click.echo('Complete.')
