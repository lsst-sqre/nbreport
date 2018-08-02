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
        json={'instance_id': '1'},
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
            '-c', 'title', 'My sick report',
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

        nb = instance.open_notebook()
        assert nb.cells[0].source == (
            "# My sick report\n"
            "\n"
            "- By: Test Bot\n"
            "- Date: 2018-07-18"
        )


@responses.activate
def test_init_command_no_template_vars(
        write_user_config, testr_000_path, runner, fake_registration):
    """Test creating a new report instance, but without rendering the
    template variables.
    """
    responses.add(
        responses.POST,
        'https://api.lsst.codes/nbreport/reports/testr-000/instances/',
        json={'instance_id': '1'},
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
            "# {{ cookiecutter.title }}\n"
            "\n"
            "- By: {{ cookiecutter.username }}\n"
            "- Date: {{ cookiecutter.generated_iso8601 }}"
        )
