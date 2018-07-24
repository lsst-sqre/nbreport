"""APIs for computing (running) notebooks.
"""

__all__ = ('compute_notebook_file', 'compute_notebook')

import logging
from pathlib import Path
from tempfile import TemporaryDirectory
import uuid

from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import nbformat


def compute_notebook_file(path, as_version=None, **compute_args):
    """Compute an ipynb notebook file and save it in place.

    Parameters
    ----------
    path : `pathlib.Path` or `str`
        Path of the notebook (ipynb) file. The computed notebook is saved
        in-place at this path as well.
    as_version : int, optional
        Notebook version to coerce the file into. `None` means
        `nbformat.NO_CONVERT`. See the `nbformat.read` documentation.
    **compute_args
        Keyword arguments passed to `compute_notebook`.
    """
    if isinstance(path, Path):
        path_str = str(path.resolve())

    if as_version is None:
        as_version = nbformat.NO_CONVERT

    notebook = nbformat.read(path_str,
                             as_version=as_version)
    notebook = compute_notebook(notebook, **compute_args)
    nbformat.write(notebook, path_str)


def compute_notebook(notebook, dirname=None, kernel_name='', timeout=None):
    """Compute a notebook object.

    Parameters
    ----------
    notebook : `nbformat.NotebookNode`
        Notebook instance.
    dirname : `pathlib.Path` or `str`, optional
        Directory to use for computing the directory. If one is not provided
        a temporary directory is created.
    kernel_name : `str`, optional
        Name of the Jupyter kernel to use when computing the notebook.
        When not specified, the default Python kernel is used.
    timeout : int, optional
        Cell execution timeout. By default there is no timeout.

    Returns
    -------
    notebook : `nbformat.NotebookNode`
        Notebook instance with cell outputs computed.

    Raises
    ------
    nbconvert.preprocessors.CellExecutionError
        Raised if there is an error running the notebook itself.
    """
    preprocessor = ExecutePreprocessor(
        timeout=timeout,
        kernel_name=kernel_name)

    if dirname is None:
        with TemporaryDirectory() as temp_dirname:
            return _run_preprocessor(preprocessor, notebook, temp_dirname)
    else:
        return _run_preprocessor(preprocessor, notebook, dirname)


def _run_preprocessor(preprocessor, notebook, dirname):
    logger = logging.getLogger(__name__)
    metadata = {
        'metadata': {
            'path': dirname
        }
    }
    try:
        preprocessor.preprocess(notebook, metadata)

    except CellExecutionError:
        uid = uuid.uuid4()
        output_path = Path('errored-{uid!s}.ipynb'.format(uid=uid)).resolve()
        nbformat.write(notebook, output_path)
        message = (
            'Error executing the notebook. See the notebook'
            '\n\n\t{output_path!s}\n\n'
            'for the traceback.'
        )
        logger.error(message)
        raise

    return notebook
