"""Implementation for the nbreport login command, which obtains a GitHub
personal access token on behalf of a user.
"""

__all__ = ('login',)

import datetime
from getpass import getuser
from socket import gethostname
from pathlib import Path

import click
import requests
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap


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

    try:
        token_data = request_github_token(
            github_username, github_password, twofactor=None)
    except GitHubTwoFactorRequired:
        twofactor = click.prompt('Your GitHub two-factor auth code', type=str)
        token_data = request_github_token(
            github_username, github_password, twofactor=twofactor)

    write_token(
        github_username,
        token_data['token'],
        token_data['note'])
    click.echo(
        'Saved the user:read token to ~/.nbreport.yaml. You '
        'can revoke it at https://github.com/settings/tokens'
    )


def request_github_token(github_username, github_password, twofactor=None):
    """Request a new GitHub personal access token on behalf of a user.

    Parameters
    ----------
    github_username : `str`
        User's GitHub username.
    github_password : `str`
        User's GitHub password.
    twofactor : `str`, optional
        The current two-factor code.

    Returns
    -------
    `dict`
        JSON body of the GitHub `POST /authorizations
        <https://developer.github.com/v3/oauth_authorizations/#create-a-new-authorization>`_
        endpoint. The token itself is in ``'token'`` key.

    Raises
    ------
    GitHubTwoFactorRequired
        Raised if a ``twofactor`` argument is required, but not given.

    Notes
    -----
    The token is generated with the ``read:user`` scope.

    The token is generated with a note formatted as::

        nbreport for {{user}}@{{hostname}} on {{ISO8601}}

    The token can be revoked at https://github.com/settings/tokens.
    """
    note = 'nbreport for {user}@{machine} on {time}'.format(
        user=getuser(),
        machine=gethostname(),
        time=datetime.datetime.now().isoformat()
    )
    request_data = {
        'scopes': ['read:user'],
        'note': note,
        'note_url': 'https://nbreport.lsst.io'
    }
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    if twofactor is not None:
        headers['X-GitHub-OTP'] = str(twofactor)
    response = requests.post(
        'https://api.github.com/authorizations',
        auth=(github_username, github_password),
        headers=headers,
        json=request_data
    )

    # Handle two-factor authentication
    if response.status_code == 401 and 'X-GitHub-OTP' in response.headers:
        raise GitHubTwoFactorRequired
    # Handle other errors
    response.raise_for_status()

    return response.json()


class GitHubTwoFactorRequired(Exception):
    """Two-factor authentication is required for this GitHub request.
    """


def write_token(username, token, note, path=None):
    """Write a GitHub personal access token to the user's nbreport
    configuration file.

    Parameters
    ----------
    username : `str`
        GitHub username.
    token : `str`
        GitHub personal access token belonging to the user.
    note : `str`
        Note to associate with the token.
    path : `str`, optional
        Path to the nbreport configuration file. By default this is located
        at ``~/.nbreport.yaml``.
    """
    yaml = ruamel.yaml.YAML()  # round-trip mode.

    if path is None:
        path = Path.home() / '.nbreport.yaml'
    else:
        path = Path(path)

    if path.exists():
        config_data = yaml.load(path)
    else:
        config_data = CommentedMap({'github': None})

    config_data['github'] = CommentedMap({
        'username': username,
        'token': token
    })
    config_data['github'].yaml_add_eol_comment(note, 'token')

    yaml.dump(config_data, path)
