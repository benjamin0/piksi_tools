Tools for the Piksi GNSS receiver
=================================

.. image:: https://travis-ci.org/swift-nav/piksi_tools.png
    :target: https://travis-ci.org/swift-nav/piksi_tools

.. image:: https://badge.fury.io/py/piksi_tools.png
    :target: https://pypi.python.org/pypi/piksi_tools

Python tools for the Piksi GNSS receiver.

Setup
-----

Install dependencies only::

  $ ./setup.sh -x install

Install from repo::

  $ sudo python setup.py install

Install package from pypi::

  $ sudo pip install piksi_tools

Usage Examples
--------------

Bootloader example
~~~~~~~~~~~~~~~~~~

Console example
~~~~~~~~~~~~~~~

To use the Piksi console, binary installers (Windows and OS X) are here_.

.. _here: https://s3-us-west-1.amazonaws.com/downloads.swiftnav.com/piksi_console/

Testing
-------

To run the tests and check for coverage::

  $  tox

License
-------

Copyright © 2015 Swift Navigation

Distributed under LGPLv3.0.
