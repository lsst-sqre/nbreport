"""Implementation for the nbreport login command, which obtains a GitHub
personal access token on behalf of a user.
"""

__all__ = ('login',)

import datetime
from getpass import getuser
from socket import gethostname

import click
import requests

from ..userconfig import insert_github_config, write_config


@click.command()
@click.pass_context
def login(ctx):
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
    github_username = click.prompt('Your GitHub username')
    github_password = click.prompt('Your GitHub password', hide_input=True)

    click.echo('Getting a personal access token from GitHub...')

    try:
        token_data = request_github_token(
            github_username, github_password, twofactor=None)
    except GitHubTwoFactorRequired:
        twofactor = click.prompt('Your GitHub two-factor auth code', type=str)
        token_data = request_github_token(
            github_username, github_password, twofactor=twofactor)

    config = insert_github_config(
        ctx.obj['config'],
        github_username,
        token_data['token'],
        token_note=token_data['note'])
    write_config(config, path=ctx.obj['config_path'])

    click.echo(
        'Saved the token to ~/.nbreport.yaml. It has read:user and read:org '
        'scope. You can revoke it at https://github.com/settings/tokens'
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
    The token is generated with the ``read:user`` and ``read:org`` scopes.

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
        'scopes': ['read:user', 'read:org'],
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
