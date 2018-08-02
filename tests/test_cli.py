"""Test the basic nbreport command.
"""

import nbreport
import nbreport.cli.main


def test_version(runner):
    """Test the version string output.
    """
    result = runner.invoke(
        nbreport.cli.main.main,
        ['--version']
    )
    assert result.exit_code == 0
    assert result.output == nbreport.__version__ + '\n'
