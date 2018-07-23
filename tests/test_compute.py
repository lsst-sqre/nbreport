"""Tests for the nbreport.compute module.
"""

from pathlib import Path

import nbformat

from nbreport.compute import compute_notebook_file


def test_compute_notebook_file(tmpdir):
    """Basic test of compute_notebook_file() that creates a notebook
    programatically, writes it, and executes it.
    """
    notebook_path = Path(tmpdir) / 'notebook.ipynb'

    notebook = nbformat.v4.new_notebook()
    notebook.cells.append(
        nbformat.v4.new_code_cell(
            '1 + 2\n'))
    nbformat.write(notebook, str(notebook_path))

    compute_notebook_file(notebook_path)

    nb = nbformat.read(str(notebook_path), as_version=nbformat.NO_CONVERT)
    assert nb.cells[0].outputs[0]['data']['text/plain'] == '3'
