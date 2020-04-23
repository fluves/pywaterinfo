import logging

import certifi

"""
INFO: Additional utilities for waterinfo
"""

logger = logging.getLogger(__name__)


class SSLAdditionException(Exception):
    """Raised when the SSL custom CA addition fails"""

    pass


def add_ssl_cert(ssl_cert: str):
    """
    This routine is a pragmatic solution to add a custom SSL certificate to the
    certifi store, which urllib needs to connect over https. Use this routine when
    git you are experiencing an issue with an SSL: CERTIFICATE_VERIFY_FAILED
    error. This should only be done once for your environment.

    For more details, see also :
    https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error

    The ssl certificate should ususally be issued by your company, please contact your
    network adminstrator.

    Parameters
    ----------
    ssl_cert: str
        The full path/filename to the SSL certificate file to add

    Examples
    --------
    >>> from pywaterinfo.utils import add_ssl_cert
    >>> add_ssl_cert("CA-FILE-PATH")  # doctest: +SKIP
    """

    try:
        logger.debug("Adding custom certs to certifi store...")
        cafile = certifi.where()
        with open(ssl_cert, "rb") as infile:
            customca = infile.read()
        with open(cafile, "ab") as outfile:
            outfile.write(customca)
        logger.debug("SSL certificate added to store.")
    except SSLAdditionException:
        logger.debug("Adding custom SSL certificate failed.")
