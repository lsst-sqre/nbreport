"""Rendering templated cells in Jupyter notebooks.
"""

__all__ = ('render_notebook', 'render_cell', 'load_template_environment')

from pathlib import Path

from cookiecutter.generate import generate_context
from cookiecutter.environment import StrictEnvironment


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


def load_template_environment(context_path=None,
                              extra_context=None):
    """Load the context (``cookiecutter.json``) and Jinja template environment.

    Parameters
    ----------
    context_path : `pathlib.Path` or `str`, optional
        Path to the ``cookiecutter.json`` context file, if available. If a path
        isn't provided, no template context is gathered from a
        ``cookiecutter.json`` file.

    extra_context : `dict`, optional
        A dictionary of key-value terms (equivalent to the
        ``cookiecutter.json`` file's structure) that override values obtained
        from any ``cookiecutter.json`` file (at ``context_path``).

        If ``context_path`` is None, then the context is populated entirely
        from ``extra_context``.

    Returns
    -------
    context : `dict`
        The context is a dictionary with a key called ``'cookiecutter'`` that
        is a `dict` with template key-value pairs obtained from the
        combination of the ``context_path`` and ``extra_context``.

        This context dictionary can be used directly by Jinja to render a
        template.

    jinja_env : `cookiecutter.environment.StrictEnvironment`
        The Jinja template environment that is pre-loaded with the context.

    Notes
    -----
    Internally this function uses `cookiecutter.generate.generate_context` to
    combine a ``cookiecutter.json`` file with ``extra_context``.
    """
    if context_path is not None:
        # Regular code path that generates a context from a combination
        # of the cookiecutter.json file with overrides.
        if isinstance(context_path, Path):
            # Compatibility for pathlib
            context_path = str(context_path.resolve())
        context = generate_context(context_file=context_path,
                                   extra_context=extra_context)

    else:
        # Programatically create a context with a JSON context file.
        if extra_context is None:
            extra_context = {}
        context = dict(cookiecutter=extra_context)

    # Also make the Jinja environment
    jinja_env = StrictEnvironment(
        context=context,
        keep_trailing_newline=True,
    )

    return context, jinja_env
