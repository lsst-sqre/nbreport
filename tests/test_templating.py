"""Tests for the nbreport.templating module.
"""

import nbformat
import pytest

from nbreport.templating import (render_cell, render_notebook,
                                 load_template_environment)


def test_render_cell_markdown():
    """Test render_cell with a Markdown cell.
    """
    context = {
        'title': 'Hello world'
    }
    context, jinja_env = load_template_environment(extra_context=context)

    original_cell = nbformat.v4.new_markdown_cell(
        '# {{ cookiecutter.title }}\n')
    rendered_cell = render_cell(original_cell, context, jinja_env)

    assert rendered_cell.source == '# Hello world\n'


def test_render_cell_code():
    """Test render_cell with a code (Python) cell.
    """
    context = {
        'a': '10',
        'b': '32'
    }
    context, jinja_env = load_template_environment(extra_context=context)

    original_cell = nbformat.v4.new_code_cell(
        'answer = {{ cookiecutter.a }} + {{ cookiecutter.b }}\n')
    rendered_cell = render_cell(original_cell, context, jinja_env)

    assert rendered_cell.source == 'answer = 10 + 32\n'


def test_render_notebook():
    """Test the render_notebook function.
    """
    context = {
        'title': 'Hello world',
        'a': '10',
        'b': '32'
    }
    context, jinja_env = load_template_environment(extra_context=context)

    notebook = nbformat.v4.new_notebook()
    notebook.cells.append(
        nbformat.v4.new_markdown_cell(
            '# {{ cookiecutter.title }}\n'))
    notebook.cells.append(
        nbformat.v4.new_code_cell(
            'answer = {{ cookiecutter.a }} + {{ cookiecutter.b }}\n'))

    rendered = render_notebook(notebook, context, jinja_env)

    assert rendered.cells[0].source == '# Hello world\n'
    assert rendered.cells[1].source == 'answer = 10 + 32\n'


@pytest.mark.parametrize(
    'use_pathlib',
    [(True,), (False,)]
)
def test_load_template_environment_from_fs(use_pathlib, testr_000_path):
    """Test loading the template environment in tests/TESTR-000 using the
    ``cookiecutter.json`` file as context.

    Test passing the context file's path as both a pathlib.Path and as a
    string.
    """
    context_path = testr_000_path / 'cookiecutter.json'

    if not use_pathlib:
        context_path = str(context_path)

    context, jinja_env = load_template_environment(context_path=context_path)

    assert context['cookiecutter']['username'] == 'Test Bot'
    assert context['cookiecutter']['date'] == '2018-07-18'
    assert context['cookiecutter']['a'] == 10
    assert context['cookiecutter']['b'] == 32


def test_load_empty_template_environment():
    """Test load_template_environment if not context is given.
    """
    context, jinja_env = load_template_environment()
    assert len(context['cookiecutter'].keys()) == 0
