"""Tests for the ``nbreport issue`` command.
"""

from pathlib import Path
import shutil

import nbformat
import responses

import nbreport.cli.main
from nbreport.repo import ReportRepo


@responses.activate
def test_issue(write_user_config, testr_000_path, runner,
               fake_registration):
    """Test a typical nbreport issue command with the tests/TESTR-000 repo.
    """
    responses.add(
        responses.POST,
        'https://api.lsst.codes/nbreport/reports/testr-000/instances/',
        json={
            'instance_id': '1',
            'ltd_edition_url': 'https://keeper.lsst.codes/editions/12345',
            'published_url': 'https://testr-000.lsst.io/v/1'
        },
        status=201)
    responses.add(
        responses.POST,
        'https://api.lsst.codes/nbreport/reports/testr-000/'
        'instances/1/notebook',
        json={
            'queue_url': 'https://example.com/queue/12345'
        },
        status=202)

    with runner.isolated_filesystem():
        # Copy the repo into this isolated workspace
        repo_path = Path.cwd() / 'TESTR-000'
        shutil.copytree(str(testr_000_path), str(repo_path))
        assert repo_path.exists()

        # Make a repo with faked registration
        repo = ReportRepo(repo_path)
        fake_registration(repo)

        # Create a mock .nbreport.yaml file with auth data
        write_user_config('.nbreport.yaml')

        args = [
            '--config-file', '.nbreport.yaml',
            'issue',  # subcommand
            str(repo_path),  # first argument
            '-c', 'a', '100',
            '-c', 'b', '200',
        ]
        result = runner.invoke(nbreport.cli.main.main, args)
        assert result.exit_code == 0

        upload_request = responses.calls[1].request
        assert upload_request.url == (
            'https://api.lsst.codes/nbreport/reports/testr-000/'
            'instances/1/notebook')

        # Check that the notebook *sent to the server* is computed properly
        nb = nbformat.reads(
            upload_request.body.decode('utf-8'),
            as_version=nbformat.NO_CONVERT)
        assert nb.cells[0].source == (
            "**TESTR-000-1**\n\n"
            "# Test Report\n\n"
            "- By: Test Bot\n"
            "- Date: 2018-07-18"
        )
        assert nb.cells[1].outputs[0].text == 'The answer is 300\n'
