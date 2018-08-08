.. _api-reference:

####################
Python API reference
####################

.. _nbreport.compute:

nbreport.compute
================

The ``nbreport.compute`` module supports running Jupyter notebooks to compute output cells.

.. automodapi:: nbreport.compute
   :no-main-docstr:
   :no-heading:
   :no-inheritance-diagram:

.. _nbreport.processing:

nbreport.processing
===================

The ``nbreport.processing`` module provides internal helpers for the command line apps.

.. automodapi:: nbreport.processing
   :no-main-docstr:
   :no-heading:
   :no-inheritance-diagram:

.. _nbreport.repo:

nbreport.repo
=============

The ``nbreport.repo`` module provides APIs for managing report repositories.

.. automodapi:: nbreport.repo
   :no-main-docstr:
   :no-heading:
   :no-inheritance-diagram:

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

.. _nbreport.userconfig:

nbreport.userconfig
===================

The ``nbreport.userconfig`` module provides interfaces to the ``~/.nbreport.yaml`` file, which is used to store GitHub credentials.

.. automodapi:: nbreport.userconfig
   :no-main-docstr:
   :no-heading:
   :no-inheritance-diagram:
