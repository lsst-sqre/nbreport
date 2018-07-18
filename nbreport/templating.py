"""Rendering templated cells in Jupyter notebooks.
"""

__all__ = ('render_notebook', 'render_cell',)


def render_notebook(notebook, context, jinja_env):
    """Render the Jinja-templated cells of a notebook.

    Parameters
    ----------
    notebook : `nbformat.NotebookNode`
        The notebook document. This can be created programatically via
        `nbformat.v4.new_notebook` or created from an ``ipynb`` file with
        `nbformat.read`. This ``notebook`` is modified in place, though
        the function also returns the modified ``notebook``.
    context : `dict`-like
        The template context. Usually this is constructed via
        `cookiecutter.generate.generate_context`.
    jinja_env : `cookiecutter.environment.StrictEnvironment`
        The Jinja environment.

    Returns
    -------
    notebook : `nbformat.NotebookNode`
        The notebook document with templated cells rendered.

    Notes
    -----
    This function operates on the ``source`` member of each cell in the
    notebook. Cell sources are treated as individual Jinja templates.
    """
    for cell in notebook.cells:
        render_cell(cell, context, jinja_env)
    return notebook


def render_cell(cell, context, jinja_env):
    """Render the Jinja-templated source of a single notebook cell.

    Parameters
    ----------
    cell : `nbformat.NotebookNode`
        An individual cell from a notebook, as a `~nbformat.NotebookNode`.
        This object can also be created programatically, see
        `nbformat.v4.new_code_cell`, `nbformat.v4.new_markdown_cell`, and
        `nbformat.v4.new_raw_cell`.
    context : `dict`-like
        The template context. Usually this is constructed via
        `cookiecutter.generate.generate_context`.
    jinja_env : `cookiecutter.environment.StrictEnvironment`
        The Jinja environment.

    Returns
    -------
    cell : `nbformat.NotebookNode`
        The input cell with the ``source`` member replaced with rendered
        content.

    Notes
    -----
    This function operates on the ``source`` member of the provided ``cell``.
    Other members of the cell are left unmodified.

    For more information about the format of a cell, see `The Notebook
    file format <https://ls.st/g01>`_ in the nbformat docs.
    """
    template = jinja_env.from_string(cell.source)
    cell.source = template.render(**context)
    return cell
