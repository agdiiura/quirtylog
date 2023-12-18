***********
quirtylog
***********

**Last Update**: |today|

**Version**: |version|

:mod: A package for quick and dirty logging with python.

Installation
~~~~~~~~~~~~~~~~

Run the install command

.. code-block:: bash
   :linenos:

   pip install quirtylog

.. currentmodule:: quirtylog

Example
~~~~~~~~~~~
.. code-block:: python
   :linenos:

   # Create custom logger object
   import quirtylog
   log_path = "/path/to/logs"
   logger = quirtylog.create_logging(log_path=log_path)

   # Handle exception
   @quirtylog.exception(logger)
   def f(x):
      """A function that raise an exception"""
      return x/0.

   f(42)

quirtylog
~~~~~~~~~~~
.. autosummary::
   :toctree: quirtylog/

   quirtylog.core
   quirtylog.singleton
   quirtylog.sqlite_logger
   quirtylog.tqdm_logger
