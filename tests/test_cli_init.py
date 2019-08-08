"""Tests for the ``nbreport init`` command.
"""

from pathlib import Path
import shutil

import nbreport.cli.main
from nbreport.repo import ReportRepo
from nbreport.instance import ReportInstance

import responses


@responses.activate
def test_init_command(write_user_config, testr_000_path, runner,
                      fake_registration):
    """Test creating a new report instance.
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

    with runner.isolated_filesystem():
        # Copy the repo into workspace
        # copy the repo into this isolated workspace
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
            'init',  # subcommand
            str(repo_path),  # first argument
            '-c', 'a', '100',
            '-c', 'b', '200',
        ]
        result = runner.invoke(nbreport.cli.main.main, args)
        assert result.exit_code == 0

        instance_path = Path('TESTR-000-1')
        assert instance_path.exists()
        instance = ReportInstance(instance_path)
        assert instance.config['instance_id'] == '1'
        assert instance.config['instance_handle'] == 'TESTR-000-1'

        # Check that the cookiecutter.json context got added to nbreport.yaml
        # This is just a sampling of the expected context
        assert 'cookiecutter' in instance.config
        assert instance.config['cookiecutter']['username'] \
            == 'Test Bot'
        assert instance.config['cookiecutter']['a'] == '100'
        assert instance.config['cookiecutter']['b'] == '200'

        nb = instance.open_notebook()

        # Check that the cells got rendered
        assert nb.cells[0].source == (
            "**TESTR-000-1**\n\n"
            "# Test Report\n\n"
            "- By: Test Bot\n"
            "- Date: 2018-07-18"
        )

        # Check that the instance config got added to the notebook metadata
        # (sampling keys)
        assert 'nbreport' in nb.metadata


@responses.activate
def test_init_command_no_template_vars(
        write_user_config, testr_000_path, runner, fake_registration):
    """Test creating a new report instance, but without rendering the
    template variables.
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

    with runner.isolated_filesystem():
        # Copy the repo into workspace
        # copy the repo into this isolated workspace
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
            'init',  # subcommand
            str(repo_path),  # first argument
        ]
        result = runner.invoke(nbreport.cli.main.main, args)
        assert result.exit_code == 0

        instance_path = Path('TESTR-000-1')
        assert instance_path.exists()
        instance = ReportInstance(instance_path)
        assert instance.config['instance_id'] == '1'
        assert instance.config['instance_handle'] == 'TESTR-000-1'

        nb = instance.open_notebook()
        assert nb.cells[0].source == (
            "**{{ instance_handle }}**\n\n"
            "# {{ title }}\n"
            "\n"
            "- By: {{ cookiecutter.username }}\n"
            "- Date: {{ cookiecutter.date }}"
        )
