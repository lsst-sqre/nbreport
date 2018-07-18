"""Tests for the nbreport.templating module.
"""

from cookiecutter.environment import StrictEnvironment
import nbformat

from nbreport.templating import render_cell


def test_render_cell_markdown():
    """Test render_cell with a Markdown cell.
    """
    context = {
        'cookiecutter': {
            'title': 'Hello world'
        }
    }
    jinja_env = StrictEnvironment(
        context=context,
        keep_trailing_newline=True,
    )

    original_cell = nbformat.v4.new_markdown_cell(
        '# {{ cookiecutter.title }}\n')
    rendered_cell = render_cell(original_cell, context, jinja_env)

    assert rendered_cell.source == '# Hello world\n'


def test_render_cell_code():
    """Test render_cell with a code (Python) cell.
    """
    context = {
        'cookiecutter': {
            'a': '10',
            'b': '32'
        }
    }
    jinja_env = StrictEnvironment(
        context=context,
        keep_trailing_newline=True,
    )

    original_cell = nbformat.v4.new_code_cell(
        'answer = {{ cookiecutter.a }} + {{ cookiecutter.b }}\n')
    rendered_cell = render_cell(original_cell, context, jinja_env)

    assert rendered_cell.source == 'answer = 10 + 32\n'
