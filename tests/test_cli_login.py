"""Test the nbreport login command.
"""

from pathlib import Path

import pytest
import responses

from nbreport.cli.login import request_github_token, GitHubTwoFactorRequired
import nbreport.cli.main


@responses.activate
def test_login_command(runner):
    """Test the nbreport login command (with mocks).
    """
    responses.add(
        responses.POST,
        'https://api.github.com/authorizations',
        json={'token': 'mytoken',
              'note': 'note for token'},
        status=201)

    with runner.isolated_filesystem():
        args = [
            '--config-file', 'nbreport.yaml',  # test-local config file
            'login',  # subcommand
        ]
        result = runner.invoke(
            nbreport.cli.main.main,
            args,
            input='testuser\ntestpassword\n')
        assert result.exit_code == 0

        config_path = Path('nbreport.yaml')
        assert config_path.exists()

        with open(config_path) as fp:
            config_text = fp.read()
        assert config_text == (
            'github:\n'
            '  username: testuser\n'
            '  token: mytoken  # note for token\n'
        )


@responses.activate
def test_request_github_token():
    """Test getting a token for a user that doesn't use 2FA.
    """
    responses.add(
        responses.POST,
        'https://api.github.com/authorizations',
        json={'token': 'mytoken',
              'note': 'note for token'},
        status=201)

    data = request_github_token('user', 'password')

    assert len(responses.calls) == 1
    assert data['token'] == 'mytoken'
    assert data['note'] == 'note for token'
    assert responses.calls[0].request.url \
        == 'https://api.github.com/authorizations'
    assert b'read:user' in responses.calls[0].request.body
    assert b'read:org' in responses.calls[0].request.body


@responses.activate
def test_request_github_token_needs_2fa():
    """Test that a login requiring 2FA is identified.
    """
    responses.add(
        responses.POST,
        'https://api.github.com/authorizations',
        status=401,
        headers={'X-GitHub-OTP': 'required; :2fa-app'})

    with pytest.raises(GitHubTwoFactorRequired):
        request_github_token('user', 'password')


@responses.activate
def test_request_github_token_with_2fa():
    """Test request_github_token when providing a one-time password.
    """
    responses.add(
        responses.POST,
        'https://api.github.com/authorizations',
        json={'token': 'mytoken',
              'note': 'note for token'},
        status=201)

    data = request_github_token('user', 'password', twofactor='123456')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers['X-GitHub-OTP'] == '123456'
    assert responses.calls[0].request.url \
        == 'https://api.github.com/authorizations'
    assert data['token'] == 'mytoken'
    assert data['note'] == 'note for token'
