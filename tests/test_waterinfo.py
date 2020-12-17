# -*- coding: utf-8 -*-

import os

import pytest

import pandas as pd
from pandas.api import types
from pandas.api.types import is_datetime64tz_dtype

from pywaterinfo import HIC_BASE, VMM_BASE, Waterinfo


def test_waterinfo_repr(vmm_connection, hic_connection):
    """Check repr/print message is correct to source"""
    assert repr(vmm_connection) == f"<Waterinfo object, Query from '{VMM_BASE}'>"
    assert repr(hic_connection) == f"<Waterinfo object, Query from '{HIC_BASE}'>"


def test_valid_sources():
    """Check error handling on improper data provider"""
    with pytest.raises(Exception) as e:
        assert Waterinfo("JAN")
        assert str(e.value) == "Provider is either 'vmm' or 'hic'."


def test_default_api_arguments(vmm_connection):
    """Check if default arguments end up in query"""
    _, res = vmm_connection.request_kiwis({"request": "getRequestInfo"})
    default_arg = {
        "service": "kisters",
        "type": "QueryServices",
        "format": "json",
        "datasource": vmm_connection._datasource,
        "timezone": "UTC",
    }
    assert all([key in res.url for key in default_arg.keys()])
    assert all([value in res.url for value in default_arg.values()])


def test_ssl_handling():
    # TODO
    NotImplemented


def test_token_vmm():
    """Check if submitting of a token is tackled properly"""
    # no token, no token header, no authentication in request header
    vmm = Waterinfo("vmm")
    assert vmm._token_header is None
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" not in res.request.headers.keys()

    # token, token header, authentication in request header
    # this client code is received by VMM for unit testing purposes only
    client = (
        "MzJkY2VlY2UtODI2Yy00Yjk4LTljMmQtYjE2OTc4ZjBjYTZhOjRhZGE"
        "4NzFhLTk1MjgtNGI0ZC1iZmQ1LWI1NzBjZThmNGQyZA=="
    )
    vmm = Waterinfo("vmm", token=client)
    assert vmm._token_header is not None
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" in res.request.headers.keys()

    # wrong token results in error
    with pytest.raises(Exception):
        client = "DUMMY"
        Waterinfo("vmm", token=client)


@pytest.mark.nohictoken
def test_token_hic():
    """Check if submitting of a token is tackled properly"""
    # no token, no token header, no authentication in request header
    hic = Waterinfo("hic")
    assert hic._token_header is None
    _, res = hic.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" not in res.request.headers.keys()

    # token, token header, authentication in request header
    # this client code is received by VMM for unit testing purposes only
    client = os.environ.get("HIC_TOKEN")
    hic = Waterinfo("hic", token=client)
    assert hic._token_header is not None
    _, res = hic.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" in res.request.headers.keys()

    # wrong token results in error
    with pytest.raises(Exception):
        client = "DUMMY"
        Waterinfo("hic", token=client)


class TestPeriodDates:
    def test_example_period_strings(self, vmm_connection):
        """VMM tutorial valid examples"""
        assert vmm_connection._check_period_format("P3D") == "P3D"
        assert vmm_connection._check_period_format("P1Y") == "P1Y"
        assert vmm_connection._check_period_format("P1DT12H") == "P1DT12H"
        assert vmm_connection._check_period_format("PT6H") == "PT6H"
        assert (
            vmm_connection._check_period_format("P1Y6M3DT4H20M30S")
            == "P1Y6M3DT4H20M30S"
        )

    def test_day_week_combi(self, vmm_connection):
        """Days and week info can not be combined"""
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P2W2D")

    def test_p_symbol(self, vmm_connection):
        """Periods are defined by P symbol"""
        with pytest.raises(Exception):
            vmm_connection._check_period_format("3D")

    def test_time_definition(self, vmm_connection):
        """Periods need at least a time definition"""
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P")

    def test_time_definition_number(self, vmm_connection):
        """Time definitions are preceded by number"""
        with pytest.raises(Exception):
            vmm_connection._check_period_format("PY")
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P3YM")
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P3Y4MD")
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P3Y4MD")
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P3Y4M5DTH")
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P3Y4M5DT4HM")
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P3Y4M5DT4H3MS")

    def test_time_subday_definition(self, vmm_connection):
        """Subday information requires the T symbol are defined by P symbol

        Actually the example, P3H, will work in waterinfo API, but this is rather
        inconsistent from the API side and the docs of VMM says otherwise
        """
        with pytest.raises(Exception):
            vmm_connection._check_period_format("P3H")

    def test_start_end_period(self, vmm_connection):
        """Impossible date/period input combinations"""
        # all three provided
        with pytest.raises(Exception):
            vmm_connection._parse_period(
                start="2012-11-01", end="2013-12-01", period="P3D"
            )
        # none of them provided
        with pytest.raises(Exception):
            vmm_connection._parse_period()
        # only end used
        with pytest.raises(Exception):
            vmm_connection._parse_period(end="2013-12-01")
        # valid combinations
        assert isinstance(
            vmm_connection._parse_period(start="2012-11-01", end="2013-12-01"), dict
        )
        assert set(
            vmm_connection._parse_period(start="2012-11-01", end="2013-12-01").keys()
        ) == set(["from", "to"])
        assert isinstance(
            vmm_connection._parse_period(start="2012-11-01", period="P3D"), dict
        )
        assert set(
            vmm_connection._parse_period(start="2012-11-01", period="P3D").keys()
        ) == set(["from", "period"])
        assert isinstance(
            vmm_connection._parse_period(end="2013-12-01", period="P3D"), dict
        )
        assert set(
            vmm_connection._parse_period(end="2013-12-01", period="P3D").keys()
        ) == set(["to", "period"])

    def test_date_formats(self, vmm_connection):
        """Date formats accepted as UTC, but provided to API as CET in order to get
        the time series as UTC

        Input datetime of the KIWIS API is always CET (and is not tz-aware), but we
        normalize everything to UTC. Hence, we interpret the package user input as UTC,
        provide the input to the API as CET and request the returned output data as UTC.
        """
        assert vmm_connection._parse_date("2017-01-01") == "2017-01-01 01:00:00"
        assert vmm_connection._parse_date("2017-08-01") == "2017-08-01 02:00:00"
        assert vmm_connection._parse_date("2017/01/01") == "2017-01-01 01:00:00"
        assert vmm_connection._parse_date("20170101") == "2017-01-01 01:00:00"
        assert vmm_connection._parse_date("2017 01 01") == "2017-01-01 01:00:00"
        assert vmm_connection._parse_date("2017-01") == "2017-01-01 01:00:00"
        assert vmm_connection._parse_date("2017") == "2017-01-01 01:00:00"
        assert (
            vmm_connection._parse_date("2017-01-01 10:00:00") == "2017-01-01 11:00:00"
        )
        assert vmm_connection._parse_date("01-01-2017") == "2017-01-01 01:00:00"

    def test_utc_return(self, df_timeseries):
        """Check that the returned dates are UTC aware and according to the user
        input in UTC
        """
        assert is_datetime64tz_dtype(df_timeseries["Timestamp"])
        assert df_timeseries.loc[0, "Timestamp"] == pd.to_datetime(
            "2019-05-01T00:00:00.000Z"
        )
        assert df_timeseries["Timestamp"].min() == pd.to_datetime(
            "2019-05-01T00:00:00.000Z"
        )
        assert types.is_datetime64tz_dtype(pd.to_datetime(df_timeseries["Timestamp"]))
        assert pd.to_datetime(df_timeseries.loc[0, "Timestamp"]).tz.zone == "UTC"

    def test_return_date_format(self, vmm_connection):
        """Input to requested return date format should be existing on KIWIS API"""
        with pytest.raises(Exception):
            vmm_connection._check_return_date_format("DUMMY")

    def test_return_fields_format(self, vmm_connection):
        """Input to requested returnfields should be existing on KIWIS API"""
        with pytest.raises(Exception):
            vmm_connection._check_return_fields_format("DUMMY,DUMMY")


class TestTimeseriesValues:
    def test_one_of_two_ids(self, vmm_connection):
        """either ts_id or timeseriesgroup_id should be used"""
        with pytest.raises(Exception):
            vmm_connection.get_timeseries_values(
                ts_id="78124042", timeseriesgroup_id="192900", period="P1D"
            )
        with pytest.raises(Exception):
            vmm_connection.get_timeseries_values(period="P1D")

    def test_multiple_ids(self, vmm_connection):
        """Call worksxpected for multiple identifiers combined in single dataframe"""
        df = vmm_connection.get_timeseries_values(
            ts_id="60992042,60968042", start="20190501 14:05", end="20190501 14:10"
        )
        assert set(df["ts_id"].unique()) == set(["60992042", "60968042"])

    def test_no_data(self, vmm_connection):
        """return empty dataframe when no data"""
        df = vmm_connection.get_timeseries_values(
            ts_id="60992042", start="21500501 14:05", end="21500501 14:10"
        )
        assert len(df) == 0
        df = vmm_connection.get_timeseries_values(
            ts_id="60992042,60968042", start="21500501 14:05", end="21500501 14:10"
        )
        assert len(df) == 0


class TestTimeseriesValueLayer:
    def test_one_of_three(self, vmm_connection):
        with pytest.raises(Exception):
            vmm_connection.get_timeseries_value_layer(
                ts_id="78124042", timeseriesgroup_id="192900", bbox="DUMMY"
            )


class TestGroupList:
    def test_group_type(self, vmm_connection):
        """Error from the KIWIS when nothing returned

        To be consistent with other sections, should be an empty dataframe.
        As this function is probably not used in returning tasks, keeping as such.
        """
        with pytest.raises(Exception):
            vmm_connection.get_group_list(group_type="DUMMY")


class TestTimeseriesList:
    def test_no_data(self, vmm_connection):
        """Empty dataframe when no data is returned"""
        assert vmm_connection.get_timeseries_list(station_no="DUMMY").equals(
            pd.DataFrame([])
        )
