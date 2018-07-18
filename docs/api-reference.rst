.. _api-reference:

####################
Python API reference
####################

.. _nbreport.templating:

nbreport.templating
===================

The ``nbreport.templating`` module provides APIs for rendering templated cells in Jupyter notebooks.

Each cell in a notebook has a ``source`` member.
This ``source`` is what a user edits in the Jupyter notebook, be it a Markdown cell or a code (Python) cell.
nbreport treats each cell's source as a Jinja template.

.. automodapi:: nbreport.templating
   :no-main-docstr:
   :no-heading:
   :no-inheritance-diagram:
