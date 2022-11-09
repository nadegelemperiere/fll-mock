=======================================================
FLL bot mocking to emulate scenarii and test functions
=======================================================

About The Project
=================

This project contains python classes emulating spike robot

.. image:: https://badgen.net/github/checks/nadegelemperiere/fll-mock
   :target: https://github.com/nadegelemperiere/fll-mock/actions/workflows/release.yml
   :alt: Status
.. image:: https://badgen.net/github/commits/nadegelemperiere/fll-mock/main
   :target: https://github.com/nadegelemperiere/fll-mock
   :alt: Commits
.. image:: https://badgen.net/github/last-commit/nadegelemperiere/fll-mock/main
   :target: https://github.com/nadegelemperiere/fll-mock
   :alt: Last commit

Built And Packaged With
-----------------------

.. image:: https://img.shields.io/static/v1?label=python&message=3.11.0&color=informational
   :target: https://www.python.org/
   :alt: Python

Testing
=======

Tested With
-----------

.. image:: https://img.shields.io/static/v1?label=python&message=3.11.0&color=informational
   :target: https://www.python.org/
   :alt: Python
.. image:: https://img.shields.io/static/v1?label=robotframework&message=6.0&color=informational
   :target: http://robotframework.org/
   :alt: Robotframework

Environment
-----------

Tests can be executed in an environment :

* in which python, pip and bash has been installed, by executing the script `scripts/robot.sh`_, or

* in which docker is available, by using the `fll test image`_ in its latest version, which already contains python, pip and bash, by executing the script `scripts/test.sh`_

.. _`fll test image`: https://github.com/nadegelemperiere/fll-test-docker
.. _`scripts/robot.sh`: scripts/robot.sh
.. _`scripts/test.sh`: scripts/test.sh

Results
-------

The test results for latest release are here_

.. _here: https://nadegelemperiere.github.io/fll-mock/report.html


Issues
======

.. image:: https://img.shields.io/github/issues/nadegelemperiere/fll-mock.svg
   :target: https://github.com/nadegelemperiere/fll-mock/issues
   :alt: Open issues
.. image:: https://img.shields.io/github/issues-closed/nadegelemperiere/fll-mock.svg
   :target: https://github.com/nadegelemperiere/fll-mock/issues
   :alt: Closed issues

Known limitations
=================

Roadmap
=======

The current version is mainly designed to read value in a scenario file. Next step is to make it more interactive, so that
functions such as start, stop,... modify the object position and the sensor acquisitions.

Contributing
============

.. image:: https://contrib.rocks/image?repo=nadegelemperiere/fll-mock
   :alt: GitHub Contributors Image

Contact
=======

Nadege Lemperiere - nadege.lemperiere@gmail.com

Acknowledgments
===============

N.A.