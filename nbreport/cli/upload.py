"""Implementation for the ``nbreport upload`` command.
"""

__all__ = ('upload',)

import click

from nbreport.instance import ReportInstance


@click.command()
@click.argument(
    'instance_path', default=None, required=True, nargs=1,
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.pass_context
def upload(ctx, instance_path):
    """Upload and publish a report instance.

    **Required arguments**

    ``INSTANCE_PATH``
        The path to the report repository directory. You can create an
        instance with the ``nbreport init`` command. The report repository
        must already be computed with the ``nbreport compute`` command.
    """
    instance = ReportInstance(instance_path)
    queue_url = instance.upload(
        github_username=ctx.obj['config']['github']['username'],
        github_token=ctx.obj['config']['github']['token'],
        server=ctx.obj['server'])

    click.echo('Upload complete.')
    click.echo('Processing status:\n  {}'.format(queue_url))
    click.echo('Publication URL:\n  {}'.format(
        instance.config['published_instance_url']))
