"""Implementation of the ``nbreport register`` command that registers a new
report with LSST the Docs.
"""

__all__ = ('register',)

from urllib.parse import urljoin

import click
import requests

from ..repo import ReportRepo


@click.command()
@click.argument(
    'repo_path', default=None, required=True, nargs=1,
)
@click.pass_context
def register(ctx, repo_path):
    """Register a report with LSST the Docs.

    This command only needs to be run once, when you're creating a new report
    repository. The command creates a new "product" on LSST the Docs where
    instances of the report are published.

    **Required arguments**

    ``REPO_PATH``
        Path to the report repository. The report repository must be a local
        directory (not a remote Git repository) because the repository's
        nbreport.yaml metadata file will be modified. The new metadata created
        by this command must be committed into the report repository.
    """
    report_repo = ReportRepo(repo_path)

    handle = report_repo.config['handle']
    title = report_repo.config['title']
    git_repo = report_repo.config['git_repo']

    try:
        github_username = ctx.obj['config']['github']['username']
        github_token = ctx.obj['config']['github']['token']
    except KeyError:
        raise click.UsageError(
            'Could not find GitHub authentication data in {0!s}. Try '
            'running "nbreport login" first.'.format(ctx.obj['config_path'])
        )

    # Allow for user confirmation
    click.echo('Registering report with this metadata from nbreport.yaml:')
    click.echo('  Handle: {}'.format(handle))
    click.echo('  Title: {}'.format(title))
    click.echo('  Git repository: {}'.format(git_repo))
    click.confirm('Register this report?', abort=True)

    response = requests.post(
        urljoin(ctx.obj['server'], '/nbreport/reports/'),
        auth=(github_username, github_token),
        json={
            'handle': handle,
            'title': title,
            'git_repo': git_repo
        }
    )
    response.raise_for_status()
    response_data = response.json()

    report_repo.config['ltd_product'] = response_data['product']
    report_repo.config['published_url'] = response_data['published_url']
    report_repo.config['ltd_url'] = response_data['product_url']

    click.echo('Registered report at {}'.format(
        report_repo.config['published_url']))
