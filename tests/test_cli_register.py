"""Tests for the ``nbreport register`` command.
"""

from pathlib import Path
import shutil

import responses

import nbreport.cli.main
from nbreport.repo import ReportRepo


@responses.activate
def test_register_command(write_user_config, testr_000_path, runner):
    """Test with no arguments except repo path.
    """
    responses.add(
        responses.POST,
        'https://api.lsst.codes/nbreport/reports/',
        json={'product': 'testr-000',
              'published_url': 'https://testr-000.lsst.io',
              'product_url': 'https://keeper.lsst.codes/products/testr-000'},
        status=201)

    with runner.isolated_filesystem():
        # copy the repo into this isolated workspace
        repo_path = Path.cwd() / 'TESTR-000'
        shutil.copytree(str(testr_000_path), str(repo_path))
        assert repo_path.exists()

        # Create a mock .nbreport.yaml file with auth data
        write_user_config('.nbreport.yaml')

        args = [
            '--config-file', '.nbreport.yaml',
            'register',  # subcommand
            str(repo_path),  # first argument
        ]
        result = runner.invoke(nbreport.cli.main.main, args, input='y\n')

        assert result.exit_code == 0

        # Test modifications to repo's nbreport.yaml
        repo = ReportRepo(repo_path)
        assert repo.config['ltd_product'] == 'testr-000'
        assert repo.config['ltd_url'] \
            == 'https://keeper.lsst.codes/products/testr-000'
        assert repo.config['published_url'] == 'https://testr-000.lsst.io'
        assert repo.config['handle'] == 'TESTR-000'
        assert repo.config['title'] == 'Test Report'
        assert repo.config['git_repo'] \
            == 'https://github.com/lsst-sqre/nbreport'
        assert repo.config['git_repo_subdir'] \
            == 'tests/TESTR-000'
