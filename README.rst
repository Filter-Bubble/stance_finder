.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - fair-software.nl recommendations
     - Badges
   * - \1. Code repository
     - |GitHub Badge|
   * - \2. License
     - |License Badge|
   * - \3. Community Registry
     - |PyPI Badge| |Research Software Directory Badge|
   * - \4. Enable Citation
     - |Zenodo Badge|
   * - \5. Checklist
     - |CII Best Practices Badge|
   * - **Other best practices**
     -
   * - Continuous integration
     - |Python Build| |PyPI Publish|


.. |GitHub Badge| image:: https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue
   :target: https://github.com/Filter-Bubble/stance_finder
   :alt: GitHub Badge

.. |License Badge| image:: https://img.shields.io/github/license/Filter-Bubble/stance_finder
   :target: https://github.com/Filter-Bubble/stance_finder
   :alt: License Badge

.. .. |PyPI Badge| image:: https://img.shields.io/pypi/v/stance_finder.svg?colorB=blue
..    :target: https://pypi.python.org/project/stance_finder/
..    :alt: PyPI Badge
.. .. |Research Software Directory Badge| image:: https://img.shields.io/badge/rsd-stance_finder-00a3e3.svg
..    :target: https://www.research-software.nl/software/stance_finder
..    :alt: Research Software Directory Badge

..
    Goto https://zenodo.org/account/settings/github/ to enable Zenodo/GitHub integration.
    After creation of a GitHub release at https://github.com/Filter-Bubble/stance_finder/releases
    there will be a Zenodo upload created at https://zenodo.org/deposit with a DOI, this DOI can be put in the Zenodo badge urls.
    In the README, we prefer to use the concept DOI over versioned DOI, see https://help.zenodo.org/#versioning.
.. .. |Zenodo Badge| image:: https://zenodo.org/badge/DOI/< replace with created DOI >.svg
..    :target: https://doi.org/<replace with created DOI>
..    :alt: Zenodo Badge

..
    A CII Best Practices project can be created at https://bestpractices.coreinfrastructure.org/en/projects/new
.. .. |CII Best Practices Badge| image:: https://bestpractices.coreinfrastructure.org/projects/< replace with created project identifier >/badge
..    :target: https://bestpractices.coreinfrastructure.org/projects/< replace with created project identifier >
..    :alt: CII Best Practices Badge

.. |Python Build| image:: https://github.com/Filter-Bubble/stance_finder/workflows/Build/badge.svg
   :target: https://github.com/Filter-Bubble/stance_finder/actions?query=workflow%3A%22Build%22
   :alt: Python Build

.. .. |PyPI Publish| image:: https://github.com/Filter-Bubble/stance_finder/workflows/Publish/badge.svg
..    :target: https://github.com/Filter-Bubble/stance_finder/actions?query=workflow%3A%22Publish%22
..    :alt: PyPI Publish

################################################################################
Stance Finder
################################################################################

Python module for finding (candidate) stances in Dutch news articles



Installation
------------

To install stance_finder, do:

.. code-block:: console

  git clone https://github.com/Filter-Bubble/stance_finder.git
  cd stance_finder
  pip install .


Run tests (including coverage) with:

.. code-block:: console

  python setup.py test


Contributing
************

If you want to contribute to the development of Stance Finder,
have a look at the `contribution guidelines <CONTRIBUTING.rst>`_.

License
*******

Copyright (c) 2021, Netherlands eScience Center

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



Credits
*******

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ and the `NLeSC/python-template <https://github.com/NLeSC/python-template>`_.
