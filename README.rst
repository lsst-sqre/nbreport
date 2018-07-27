########
nbreport
########

nbreport is a client for creating and publishing LSST's notebook-based reports.
Notebook-based reports are generated from template repositories, computed, and published with LSST the Docs.

**Documentation:** https://nbreport.lsst.io

Installation
============

nbreport is available on pypi.org::

   pip install nbreport

nbreport is made for Python 3.6 *and newer.*

Overview
========

You can use nbreport to:

1. Create an *instance* of a report from a report repository.
2. Fill that instance in with template variables that configure the report instance.
3. Compute the report instance.
4. Publish the report instance.

Try this test command to get a sense for how nbreport work::

   nbreport test https://github.com/lsst-sqre/nbreport --git-subdir tests/TESTR-000 -c title "My first report"

This test command uses the `TESTR-000 example report repository`_ in this project's own Git repository.
Next, it creates a new instance called ``TESTR-000-test`` in your current working directory and configures the notebook so that the ``title`` variable is ``"My first report"``.
Finally, the test command runs the notebook to generate outputs.

Learn more about nbreport and how to create reports with LSST's notebook-based report system at https://nbreport.lsst.io.

.. _`TESTR-000 example report repository`: https://github.com/lsst-sqre/nbreport/tree/master/tests/TESTR-000
