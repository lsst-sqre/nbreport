########
nbreport
########

nbreport is a client for creating and publishing LSST's notebook-based reports.
Notebook-based reports are generated from template repositories, computed, and published with LSST the Docs.

nbreport is developed on GitHub at https://github.com/lsst-sqre/nbreport.
The design document is https://sqr-023.lsst.io.

Installation
============

.. code-block:: bash

   pip install nbreport

nbreport is built for Python 3.6 and newer.

Try it out
==========

This one-line command creates a test report instance:

.. code-block:: bash

   nbreport test https://github.com/lsst-sqre/nbreport --git-subdir tests/TESTR-000 \
       -c username $USER -c date `date +"%F"` -c a 20

This test command uses the `TESTR-000 example report repository`_ in this project's own Git repository.
Next, it creates a new report instance called ``TESTR-000-test`` in your current working directory and configures the values for three variables in the notebook template: ``username``, ``date``, and ``a``.
Finally, the test command runs the notebook to generate outputs.

Documentation
=============

.. toctree::
   :maxdepth: 2

   repository-guide/index
   cli-reference
   api-reference
   changelog
   development

.. _`TESTR-000 example report repository`: https://github.com/lsst-sqre/nbreport/tree/master/tests/TESTR-000
