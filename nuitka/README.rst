Basic compile
=============

.. code-block:: bash

    python -m nuitka --follow-imports compileMe.py

This will give you a single .bin file.  It depends on a compatible CPython being installed.
This 79 byte Python example file becomes 161 kB

Compile with bundled Python
===========================

.. code-block:: bash

    python -m nuitka --follow-imports --standalone compileMe.py

This will give you an entire directory's worth of files, that will not depend on anything being installed on host.
This 79 byte Python example file becomes 20.7 MB