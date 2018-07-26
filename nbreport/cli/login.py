"""Implementation for the nbreport login command, which obtains a GitHub
personal access token on behalf of a user.
"""

__all__ = ('login',)

import click


@click.command()
@click.option(
    '--name', 'github_username', prompt='Your GitHub username',
    help='Your GitHub username. You’ll be prompted for it if not provided '
         'as an option.'
)
@click.password_option(
    '--password', 'github_password', prompt='Your GitHub password',
    help='Your GitHub username. You’ll be prompted for it if not provided '
         'as an option.'
)
@click.pass_context
def login(ctx, github_username, github_password):
    """Obtain a personal access token from GitHub.

    Other nbreport subcommands that publish report instances authenticate
    using your GitHub identity and organization memberships. Run this command
    first to obtain a personal access token that you can use to authenticate
    with the other commands.

    This command creates a personal access token that is stored in the
    ``~/.nbreport.yaml`` file.

    By using a personal access token, nbreport ensures that your GitHub
    password never passes through LSST's servers.  You can always revoke a
    personal access token created by this command by going to
    https://github.com/settings/tokens.
    """
    click.echo('Getting a personal access token from GitHub.')
