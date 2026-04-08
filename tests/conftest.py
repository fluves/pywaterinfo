# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest

import datetime
import os
import pandas as pd
from io import BytesIO
from pathlib import Path

from pywaterinfo.waterinfo import Waterinfo

# use a session for VMM that can be used among tests
# Tokens (None if not available)
TOKENS = {
    "vmm": (
        "MzJkY2VlY2UtODI2Yy00Yjk4LTljMmQtYjE2OTc4ZjBjYTZhOj"
        "RhZGE4NzFhLTk1MjgtNGI0ZC1iZmQ1LWI1NzBjZThmNGQyZA=="
    ),
    "hic": os.environ.get("HIC_TOKEN"),
    "vmm_grid": os.environ.get("VMM_GRID_TOKEN"),
}

CURRENT_DIR = Path(__file__).resolve().parent


@pytest.fixture
def patch_retention(monkeypatch):
    retention = datetime.timedelta(seconds=2)
    monkeypatch.setattr("pywaterinfo.waterinfo.CACHE_RETENTION", retention)


@pytest.fixture(scope="module")
def connection_factory():
    """Factory fixture to create Waterinfo connections with optional cache."""

    def _make(provider: str, cache: bool = False):
        token = TOKENS.get(provider)
        session = Waterinfo(provider, token=token, cache=cache)
        if cache:
            session.clear_cache()
        return session

    return _make


# Specific connections using the factory
@pytest.fixture(scope="module")
def vmm_connection(connection_factory):
    return connection_factory("vmm")


@pytest.fixture(scope="module")
def vmm_cached_connection(connection_factory):
    return connection_factory("vmm", cache=True)


@pytest.fixture(scope="module")
def hic_connection(connection_factory):
    return connection_factory("hic")


@pytest.fixture(scope="module")
def hic_cached_connection(connection_factory):
    return connection_factory("hic", cache=True)


@pytest.fixture(scope="module")
def vmm_grid_connection(connection_factory):
    return connection_factory("vmm_grid")


@pytest.fixture(scope="module")
def vmm_grid_cached_connection(connection_factory):
    return connection_factory("vmm_grid", cache=True)


@pytest.fixture(scope="module")
def df_timeseries(vmm_connection):
    return vmm_connection.get_timeseries_values(
        78124042, start="20190501", end="20190502"
    )


@pytest.fixture(scope="module")
def mock_vmm_grid_hdf5_response():
    """Mock VMM grid HDF5 format response"""
    with open(CURRENT_DIR / "data" / "ts_id_911010_hdf5_response.hdf5", "rb") as f:
        io_content = f.read()
    return BytesIO(io_content)


@pytest.fixture(scope="module")
def mock_vmm_grid_metadata_df():
    """Mock VMM grid metadata response for get_timeseries_value_layer"""

    return pd.DataFrame(
        [
            {
                "ts_name": "Rainfall.Radar.5min",
                "station_no": "RADAR_001",
                "station_id": "911010",
                "stationparameter_longname": "Rainfall",
                "ts_unitsymbol": "mm",
            }
        ]
    )
