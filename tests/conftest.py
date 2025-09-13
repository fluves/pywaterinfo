# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest

import datetime
import os

from pywaterinfo.waterinfo import Waterinfo

# use a session for VMM that can be used among tests
vmm_client = (
    "MzJkY2VlY2UtODI2Yy00Yjk4LTljMmQtYjE2OTc4ZjBjYTZhOj"
    "RhZGE4NzFhLTk1MjgtNGI0ZC1iZmQ1LWI1NzBjZThmNGQyZA=="
)

hic_client = os.environ.get("HIC_TOKEN")
vmm_grid_client = os.environ.get("VMM_GRID_TOKEN")


@pytest.fixture
def patch_retention(monkeypatch):
    retention = datetime.timedelta(seconds=2)
    monkeypatch.setattr("pywaterinfo.waterinfo.CACHE_RETENTION", retention)


@pytest.fixture(scope="module")
def vmm_connection():
    return Waterinfo("vmm", token=vmm_client)


@pytest.fixture(scope="module")
def vmm_cached_connection():
    session = Waterinfo("vmm", token=vmm_client, cache=True)
    session.clear_cache()
    return session


@pytest.fixture(scope="module")
def hic_connection():
    if hic_client:
        return Waterinfo("hic", token=hic_client)
    else:
        return Waterinfo("hic")


@pytest.fixture(scope="module")
def hic_cached_connection():
    if hic_client:
        session = Waterinfo("hic", token=hic_client, cache=True)
        session.clear_cache()
        return session
    else:
        session = Waterinfo("hic", cache=True)
        session.clear_cache()
        return session


@pytest.fixture(scope="module")
def vmm_grid_connection():
    if vmm_grid_client:
        session = Waterinfo("vmm_grid", token=vmm_grid_client, cache=True)
        session.clear_cache()
    else:
        session = Waterinfo("vmm_grid", cache=True)
        session.clear_cache()

    return session


@pytest.fixture(scope="module")
def vmm_grid_cached_connection():
    if vmm_grid_client:
        session = Waterinfo("vmm_grid", token=vmm_grid_client)
        session.clear_cache()
    else:
        session = Waterinfo("vmm_grid")
        session.clear_cache()

    return session


@pytest.fixture(scope="module")
def df_timeseries(vmm_connection):
    return vmm_connection.get_timeseries_values(
        78124042, start="20190501", end="20190502"
    )
