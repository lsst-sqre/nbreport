.. _how-to-use-assets:

############################################################
How to include data files with a notebook template as assets
############################################################

Your report notebook might require additional files to run.
These might be data files, like CSV, YAML, HDF5, or FITS.

One approach is to maintain these data files on a web server and use a Python library like Requests_ to download that data on demand.

In cases where the data files are highly coupled and specific to the report, though, it's natural to bundle these files with the templated report itself.
This approach ensures that data files are maintained and versioned in step with the report template since both the data and code are co-located in the same Git repository.
nbreport enables you to do this with a feature called :ref:`assets <yaml-assets>`.

This pages guides you through using the assets feature.

.. seealso::

   Another application of assets is for including Python modules alongside a notebook.
   See :doc:`how-to-use-python-modules` for details.

Step 1. Commit the data files into the Git repository of the notebook template
==============================================================================

Commit the data files into the Git repository of the notebook template.
These files must be in the same directory as the notebook (``ipynb`` file) or a subdirectory relative to the notebook file.

For example, the template repository contents might look like this:

.. code-block:: text

   .
   ├── conf.yaml
   ├── images
   │   ├── image1.files
   │   └── image2.files
   ├── nbreport.yaml
   └── TEST-000.ipynb

The assets are :file:`conf.yaml` file and the contents of the :file:`images` directory.

Step 2. Register the files as "assets" in the nbreport.yaml file
================================================================

Open the :file:`nbreport.yaml` file in the notebook template repository.
Add a key called ``assets`` to that YAML file, and then add list items to that key that match the paths of data files.
File paths, directory names, and globs are supported — see the :ref:`assets reference documentation <yaml-assets>` for details.

To match the assets in the previous example, the ``assets`` configuration might be:

.. code-block:: yaml

   assets:
     - 'conf.yaml'
     - 'images'

Alternatively, to ensure that only FITS files in the :file:`images` directory (and its subdirectories) are matched, you might instead use a glob:

.. code-block:: yaml

   assets:
     - 'conf.yaml'
     - 'images/**/*.fits'

When a new report instance is created with the `nbreport init`_ or `nbreport issue`_ commands, the files marked as assets are copied from the notebook template repository into the instance's working directory.
Directory structure is preserved.
These files **are not** processed by `Jinja templates`_.

For more information about the ``assets`` field in the :file:`nbreport.yaml` file, see the :ref:`nbreport.yaml reference <yaml-assets>`.

.. _nbreport init: ../cli-reference.html#nbreport-init
.. _nbreport issue: ../cli-reference.html#nbreport-issue
.. _Requests: https://2.python-requests.org/en/master/
.. _Jinja templates: https://palletsprojects.com/p/jinja/
