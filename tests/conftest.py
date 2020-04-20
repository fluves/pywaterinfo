# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest

from pywaterinfo.waterinfo import Waterinfo

# use a session for VMM/HIC that can be used among tests
vmm_client = (
    "MTU1MzRiYzgtZDQ2ZS00ZTEyLWI0ZmYtYzA0OWIzYzljYjI"
    "3OjQ1ZmU5M2ExLWNiNzUtNGExZi1hZDZkLWU2ODk1OGU0MWQwMg=="
)


@pytest.fixture(scope="module")
def vmm_connection():
    return Waterinfo("vmm", token=vmm_client)


@pytest.fixture(scope="module")
def hic_connection():
    return Waterinfo("hic")


@pytest.fixture(scope="module")
def df_timeseries(vmm_connection):
    return vmm_connection.get_timeseries_values(
        78124042, start="20190501", end="20190502"
    )
