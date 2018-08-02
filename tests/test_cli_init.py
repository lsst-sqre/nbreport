"""Tests for the ``nbreport init`` command.
"""

from pathlib import Path
import shutil

# import nbreport.cli.main

from click.testing import CliRunner
import responses


@responses.activate
def test_init_command(write_user_config, testr_000_path):
    """Test creating a new report instance.
    """

    runner = CliRunner()
    with runner.isolated_filesystem():
        # Copy the repo into workspace
        # copy the repo into this isolated workspace
        repo_path = Path.cwd() / 'TESTR-000'
        shutil.copytree(str(testr_000_path), str(repo_path))
        assert repo_path.exists()

        # Fake the repo's registration
        # TODO
