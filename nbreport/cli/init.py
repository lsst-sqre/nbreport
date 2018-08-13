"""Implementation of the ``nbreport init`` command that initializes a new
report instance.
"""

__all__ = ('init',)

from tempfile import TemporaryDirectory

import click

from ..repo import ReportRepo
from ..processing import is_url, create_instance


@click.command()
@click.argument(
    'repo_path_or_url', default=None, required=True, nargs=1,
)
@click.option(
    '-c', '--config', 'template_variables', nargs=2, type=str, multiple=True,
    help='Template key-value pairs. For example, if the report has a template '
         'variable called ``title``, you can provide it as ``-c title "Hello '
         'World!"``. You can provide multiple -c/--config options. If no '
         'variables are set, the notebook’s templated cells are not rendered. '
         'You can render the cells laster with the ``nbreport render`` '
         'command.'
)
@click.option(
    '-d', '--dir', 'instance_path', type=click.Path(),
    help='Path of the report directory. By default, the report directory '
         'is created in the current working directory and is named '
         '{{handle}}-{{id}}.'
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
@click.option(
    '--overwrite/--no-overwrite', default=False,
    help='Whether or not to overwrite an instance (on disk). Overwriting '
         'is disable by default. If --dir is not set, overwriting should '
         'not be necessary.'
)
@click.pass_context
def init(ctx, repo_path_or_url, template_variables, instance_path,
         git_repo_subdir, git_repo_ref, overwrite):
    """Initialize a new report instance.

    This command creates a report **instance** from a report **repository**.
    It can work with either local report repositories, or even clone a
    report repository (from GitHub, for example).

    This command contacts the nbreport server to reserve a unique **instance
    ID**.

    You can also render the report's template variables by providing
    ``-c`` / ``--config`` options. If you don't render the template variables
    now, you can do it later with the ``nbreport render`` command.

    **Required arguments**

    ``REPO_PATH_OR_URL``
        The path to the report repository directory on the file system **or**
        the URL of a remote Git repository.
    """
    template_variables = dict(template_variables)
    if len(template_variables) == 0:
        # If no variables were configured by the user, defer rendering the
        # cell templates to the nbreport render command
        template_variables = None

    create_instance_args = {
        'template_variables': template_variables,
        'instance_path': instance_path,
        'github_username': ctx.obj['config']['github']['username'],
        'github_token': ctx.obj['config']['github']['token'],
        'server': ctx.obj['server'],
        'overwrite': overwrite,
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

    click.echo('Created new report instance at {0!s}'.format(instance.dirname))

    if template_variables is None:
        click.echo(
            'Run\n  nbreport render {0!s}\n(with -c options) to render '
            'the instance’s templated cells.'.format(instance.dirname))
