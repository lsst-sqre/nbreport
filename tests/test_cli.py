"""Test the basic nbreport command.
"""

from click.testing import CliRunner

import nbreport
import nbreport.cli.main


def test_version():
    """Test the version string output.
    """
    runner = CliRunner()

    result = runner.invoke(
        nbreport.cli.main.main,
        ['--version']
    )
    assert result.exit_code == 0

    assert result.output == nbreport.__version__ + '\n'
