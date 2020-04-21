
====================
Print versus logging
====================

When developing functionalities of the package, use the `logging module <https://docs.python.org/3/library/logging.html>`_
instead of :code:`print` statements in the code.

Check the `logging howto <https://docs.python.org/3.7/howto/logging.html>`_ document
for more details. In short: by using logging on this library/package level, we can optimize the logging
of the applications making use of this package and providing them control of what kind of messages are logged on the application side.

For example, when using external API calls (e.g. waterinfo.be) and things
go wrong, it is interested to verify the HTTP call. However, when using the library code or as part of
an application, one might not bother the detailed HTTP calls. By adding the URLs of the response in an
:code:`logging.info` message, this behaviour (where to see what) can be fully controlled on the application side.

From the package side, the following is required:

::

    import logging
    logger = logging.getLogger(__name__)
    ...
    logging.info(f"Succesful waterinfo API request with call {res.url}")

On the applciation (using/relying on the package) side, one can control the level of log messages. If
interested in seeing these informative messages, set the level on :code:`logging.INFO`:

::

    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

If not, define another level, e.g. :code:`logging.DEBUG`. Much more configuration is possible.
