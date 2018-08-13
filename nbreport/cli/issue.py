"""Implementation of the ``nbreport issue`` command.
"""

__all__ = ('issue',)

from tempfile import TemporaryDirectory

import click

from nbreport.compute import compute_notebook_file
from nbreport.processing import create_instance, is_url
from nbreport.repo import ReportRepo


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
def issue(ctx, repo_path_or_url, template_variables, instance_path, timeout,
          kernel, git_repo_subdir, git_repo_ref):
    """Create, compute, and upload a report instance, all-in-one.

    **Required arguments**

    ``REPO_PATH_OR_URL``
        The path to the report repository directory on the file system **or**
        the URL of a remote Git repository.
    """
    template_variables = dict(template_variables)

    create_instance_args = {
        'template_variables': template_variables,
        'instance_path': instance_path,
        'github_username': ctx.obj['config']['github']['username'],
        'github_token': ctx.obj['config']['github']['token'],
        'server': ctx.obj['server'],
        'overwrite': False,
    }

    if is_url(repo_path_or_url):
        with TemporaryDirectory() as tempdir:
            report_repo = ReportRepo.git_clone(
                repo_path_or_url,
                clone_base_dir=tempdir,
                subdir=git_repo_subdir,
                checkout=git_repo_ref
            )
            instance = create_instance(report_repo, **create_instance_args)
    else:
        report_repo = ReportRepo(repo_path_or_url)
        instance = create_instance(report_repo, **create_instance_args)

    compute_notebook_file(instance.ipynb_path, timeout=timeout,
                          kernel_name=kernel)

    queue_url = instance.upload(
        github_username=ctx.obj['config']['github']['username'],
        github_token=ctx.obj['config']['github']['token'],
        server=ctx.obj['server'])

    click.echo('Issued report instance {}.'.format(
        instance.config['instance_handle']))
    click.echo('Processing status:\n  {}'.format(queue_url))
    click.echo('Publication URL:\n  {}'.format(
        instance.config['published_instance_url']))
