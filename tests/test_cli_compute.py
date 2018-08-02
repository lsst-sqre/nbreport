"""Tests for the nbreport compute command.
"""

from pathlib import Path

import nbreport.cli.main
from nbreport.repo import ReportRepo
from nbreport.processing import create_instance


def test_compute_command(testr_000_path, runner):
    """Test the nbreport compute command.
    """
    with runner.isolated_filesystem():
        repo = ReportRepo(testr_000_path)
        instance = create_instance(
            repo,
            instance_id='test',
            template_variables={},
            instance_path=Path('TESTR-000-test'))

        args = [
            'compute',  # subcommand
            str(instance.dirname),  # first argument
        ]
        result = runner.invoke(nbreport.cli.main.main, args)
        assert result.exit_code == 0

        # Check that the notebook was computed and saved
        nb = instance.open_notebook()
        assert nb.cells[1].outputs[0].text == 'The answer is 42\n'
