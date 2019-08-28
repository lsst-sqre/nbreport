.. _how-to-use-modules:

#######################################################
How to use Python modules in a report notebook template
#######################################################

Your report notebook might import Python modules in order to work.
Importing modules is useful because it means that code can be reused across multiple applications.
It also means that the implementation is hidden from the rendered report instances so that your report presentation can focus on results, rather than code.

There are two ways to use external Python modules from a report notebook:

1. Import from an installed package (for example, ``import astropy``, or ``from lsst.daf.butler import Butler``).
2. Import from Python modules (``*.py`` files) in the report's directory.

In the first case, nbreport doesn't currently help you set up a Python environment and install packages with ``pip``, ``conda``, or ``eups distrib install``.
It's assumed that you have set up your Python environment before running nbreport and computing a report instance.

The rest of this page deals with the second case of working with local Python modules in notebook template repositories.

Step 1. Commit the Python module into the notebook repository
=============================================================

Suppose that your notebook imports a function from a module named :file:`analysis.py`:

.. code-block:: py

   from analysis import run

In this case, commit the file :file:`analysis.py` into the report repository, alongside the Jupyter notebook file.

The report template repository contents will look like this:

.. code-block:: text

   .
   ├── analysis.py
   ├── cookiecutter.json
   ├── nbreport.yaml
   └── TEST-000.ipynb

Step 2. Designate the Python module as an asset in nbreport.yaml
================================================================

Edit the :file:`nbreport.yaml` file to designate the Python module as an *asset*.
Specifically add these lines:

.. code-block:: yaml

   assets:
     - 'analysis.py'

Alternatively, to ensure that *any* Python module is treated as an asset you can use a glob:

.. code-block:: yaml

   assets:
     - '**/*.py'

Marking Python files as assets is necessary so that these files are copied from the report repository when a report instance is rendered and computed by the `nbreport init`_ or `nbreport issue`_ commands.

Keep in mind that assets are not rendered as templates.
*Assets aren't processed by Jinja.*
The natural way to make code in a module respond to template variables is to pass those variables as arguments from the notebook code to the module code.

For more information about the ``assets`` field in the :file:`nbreport.yaml` file, see the :ref:`nbreport.yaml reference <yaml-assets>`.

.. _nbreport init: ../cli-reference.html#nbreport-init
.. _nbreport issue: ../cli-reference.html#nbreport-issue
