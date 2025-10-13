# -*- coding: utf-8 -*-
import pytest

import datetime
import logging
import os
import pandas as pd
import pytz
import sys

import pywaterinfo
from pywaterinfo import Waterinfo
from pywaterinfo.waterinfo import WaterinfoException


def test_invalid_providers():
    """Check error handling on improper data provider"""

    invalid_provider = "JAN"
    available_providers = pywaterinfo.waterinfo.PROVIDERS

    with pytest.raises(WaterinfoException) as e:
        Waterinfo(invalid_provider)
        assert str(e.value) == (
            f"Available providers: {', '.join(available_providers)}."
        )


@pytest.mark.parametrize("cache", [False, True])
@pytest.mark.parametrize("provider", ["hic", "vmm", "vmm_grid"])
def test_valid_providers(cache, provider):
    """Verify all available sources can be used to create a Waterinfo object"""
    conn = Waterinfo(provider, cache=cache)
    assert repr(conn) == (
        f"<Waterinfo object, Query "
        f"from '{pywaterinfo.waterinfo.PROVIDERS[provider]['base_url']}'>"
    )


@pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
def test_default_api_arguments(connection, request):
    """Check if default arguments end up in query"""
    connection = request.getfixturevalue(connection)
    _, res = connection.request_kiwis({"request": "getRequestInfo"})
    default_arg = {
        "service": "kisters",
        "type": "QueryServices",
        "format": "json",
        "datasource": connection._datasource,
        "timezone": "UTC",
    }
    assert all([key in res.url for key in default_arg.keys()])
    assert all([value in res.url for value in default_arg.values()])


def test_ssl_handling():
    # TODO
    NotImplemented


@pytest.mark.notoken
@pytest.mark.parametrize("cache", [False, True])
def test_token_vmm(cache):
    """Check if submitting of a token is tackled properly"""
    # no token, no token header, no authentication in request header
    vmm = Waterinfo("vmm", cache=cache)
    vmm.clear_cache()
    assert vmm._token_header is None
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" not in res.request.headers.keys()

    # token, token header, authentication in request header
    # this client code is received by VMM for unit testing purposes only
    client = os.environ.get("VMM_TOKEN")
    vmm = Waterinfo("vmm", token=client, cache=cache)
    vmm.clear_cache()
    assert vmm._token_header is not None
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" in res.request.headers.keys()

    # wrong token results in error
    with pytest.raises(Exception):
        client = "DUMMY"
        Waterinfo("vmm", token=client)


@pytest.mark.notoken
@pytest.mark.parametrize("cache", [False, True])
def test_token_hic(cache):
    """Check if submitting of a token is tackled properly"""
    # no token, no token header, no authentication in request header
    hic = Waterinfo("hic", cache=cache)
    hic.clear_cache()
    assert hic._token_header is None
    _, res = hic.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" not in res.request.headers.keys()

    # token, token header, authentication in request header
    # this client code is received by VMM for unit testing purposes only
    client = os.environ.get("HIC_TOKEN")
    hic = Waterinfo("hic", token=client, cache=cache)
    hic.clear_cache()
    assert hic._token_header is not None
    _, res = hic.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" in res.request.headers.keys()

    # wrong token results in error
    with pytest.raises(Exception):
        client = "DUMMY"
        Waterinfo("hic", token=client, cache=cache)


@pytest.mark.notoken
@pytest.mark.parametrize("cache", [False, True])
def test_token_vmm_grid(cache):
    """Check if submitting of a token is tackled properly"""
    # no token, no token header, no authentication in request header
    vmm_grid = Waterinfo("vmm_grid", cache=cache)
    vmm_grid.clear_cache()
    assert vmm_grid._token_header is None
    _, res = vmm_grid.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" not in res.request.headers.keys()

    # token, token header, authentication in request header
    # this client code is received by VMM for unit testing purposes only
    client = os.environ.get("VMM_GRID_TOKEN")
    vmm_grid = Waterinfo("vmm_grid", token=client, cache=cache)
    vmm_grid.clear_cache()
    assert vmm_grid._token_header is not None
    _, res = vmm_grid.request_kiwis({"request": "getRequestInfo"})
    assert "Authorization" in res.request.headers.keys()

    # wrong token results in error
    with pytest.raises(Exception):
        client = "DUMMY"
        Waterinfo("vmm_grid", token=client, cache=cache)


@pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
class TestPeriodDates:
    def test_example_period_strings(self, connection, request):
        """VMM tutorial valid examples"""
        connection = request.getfixturevalue(connection)
        assert connection._check_period_format("P3D") == "P3D"
        assert connection._check_period_format("P1Y") == "P1Y"
        assert connection._check_period_format("P1DT12H") == "P1DT12H"
        assert connection._check_period_format("PT6H") == "PT6H"
        assert connection._check_period_format("P1Y6M3DT4H20M30S") == "P1Y6M3DT4H20M30S"

    def test_day_week_combi(self, connection, request):
        """Days and week info can not be combined"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection._check_period_format("P2W2D")

    def test_p_symbol(self, connection, request):
        """Periods are defined by P symbol"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection._check_period_format("3D")

    def test_time_definition(self, connection, request):
        """Periods need at least a time definition"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection._check_period_format("P")

    def test_time_definition_number(self, connection, request):
        """Time definitions are preceded by number"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection._check_period_format("PY")
        with pytest.raises(Exception):
            connection._check_period_format("P3YM")
        with pytest.raises(Exception):
            connection._check_period_format("P3Y4MD")
        with pytest.raises(Exception):
            connection._check_period_format("P3Y4MD")
        with pytest.raises(Exception):
            connection._check_period_format("P3Y4M5DTH")
        with pytest.raises(Exception):
            connection._check_period_format("P3Y4M5DT4HM")
        with pytest.raises(Exception):
            connection._check_period_format("P3Y4M5DT4H3MS")

    def test_time_subday_definition(self, connection, request):
        """Subday information requires the T symbol are defined by P symbol

        Actually the example, P3H, will work in waterinfo API, but this is rather
        inconsistent from the API side and the docs of VMM says otherwise
        """
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection._check_period_format("P3H")

    def test_start_end_period(self, connection, request):
        """Impossible date/period input combinations"""
        connection = request.getfixturevalue(connection)
        # all three provided
        with pytest.raises(Exception):
            connection._parse_period(start="2012-11-01", end="2013-12-01", period="P3D")
        # none of them provided
        with pytest.raises(Exception):
            connection._parse_period()
        # only end used
        with pytest.raises(Exception):
            connection._parse_period(end="2013-12-01")
        # valid combinations
        assert isinstance(
            connection._parse_period(start="2012-11-01", end="2013-12-01"), dict
        )
        assert set(
            connection._parse_period(start="2012-11-01", end="2013-12-01").keys()
        ) == set(["from", "to"])
        assert isinstance(
            connection._parse_period(start="2012-11-01", period="P3D"), dict
        )
        assert set(
            connection._parse_period(start="2012-11-01", period="P3D").keys()
        ) == set(["from", "period"])
        assert isinstance(
            connection._parse_period(end="2013-12-01", period="P3D"), dict
        )
        assert set(
            connection._parse_period(end="2013-12-01", period="P3D").keys()
        ) == set(["to", "period"])


@pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
class TestDatetimeHandling:
    def test_input_date_formats_utc_default(self, connection, request):
        """Date formats accepted as UTC, but provided to API as CET in order to get
        the time series as UTC

        Input datetime of the KIWIS API is always CET (and is not tz-aware), but (by
        default) we normalize everything to UTC. Hence, we interpret the package user
        input as UTC, provide the input to the API as CET and request the returned
        output data as UTC.
        """
        connection = request.getfixturevalue(connection)
        assert connection._parse_date("2017-01-01") == "2017-01-01 01:00:00"
        assert connection._parse_date("2017-08-01") == "2017-08-01 02:00:00"
        assert connection._parse_date("2017/01/01") == "2017-01-01 01:00:00"
        assert connection._parse_date("20170101") == "2017-01-01 01:00:00"
        assert connection._parse_date("2017 01 01") == "2017-01-01 01:00:00"
        assert connection._parse_date("2017-01") == "2017-01-01 01:00:00"
        assert connection._parse_date("2017") == "2017-01-01 01:00:00"
        assert connection._parse_date("2017-01-01 10:00:00") == "2017-01-01 11:00:00"
        assert connection._parse_date("01-01-2017") == "2017-01-01 01:00:00"

    @pytest.mark.skipif(sys.version_info < (3, 9), reason="ZoneInfo is 3.9 feature")
    def test_utc_default_return(self, connection, df_timeseries):  # noqa
        """Check that the returned dates are UTC aware and according to the user
        input in UTC
        """
        assert isinstance(df_timeseries["Timestamp"].dtype, pd.DatetimeTZDtype)
        assert df_timeseries.loc[0, "Timestamp"] == pd.to_datetime(
            "2019-05-01T00:00:00.000Z"
        )
        assert df_timeseries["Timestamp"].min() == pd.to_datetime(
            "2019-05-01T00:00:00.000Z"
        )
        assert isinstance(df_timeseries["Timestamp"].dtype, pd.DatetimeTZDtype)
        assert (
            pd.to_datetime(df_timeseries.loc[0, "Timestamp"]).tz
            == datetime.timezone.utc
        )

    def test_kiwis_requires_cet(self, connection, caplog, request):
        """Check on the KIWIS behavior of CET date format as request parameter

        When using the KIWIS API, the input date format is always CET, whereas the
        output data format can be requested. In pywaterinfo, we change this behavior
        so when requesting a timezone, the input date format is assumed in this format
        as well and the query will be adjusted as such.
        """
        connection = request.getfixturevalue(connection)
        # Requesting data at CET 14h should equal requesting data at UTC 16h (+2h)
        with caplog.at_level(logging.INFO):
            df_utc = connection.get_timeseries_values(
                ts_id="60992042",
                start="20190501 14:05:00",
                end="20190501 14:10:00",
                returnfields="Timestamp,Value",
                timezone="UTC",
            )
            assert "timezone=UTC" in caplog.text
            # from/to request parameter adjusted to link input date format to timezone
            assert "from=2019-05-01+16%3A05%3A00" in caplog.text
            assert "to=2019-05-01+16%3A10%3A00" in caplog.text
        caplog.clear()

        with caplog.at_level(logging.INFO):
            df_cet = connection.get_timeseries_values(
                ts_id="60992042",
                start="20190501 16:05:00",
                end="20190501 16:10:00",
                returnfields="Timestamp,Value",
                timezone="CET",
            )
            assert "timezone=CET" in caplog.text
            assert "from=2019-05-01+16%3A05%3A00" in caplog.text
            assert "to=2019-05-01+16%3A10%3A00" in caplog.text
        caplog.clear()
        pd.testing.assert_series_equal(
            df_utc["Timestamp"], df_cet["Timestamp"].dt.tz_convert("UTC")
        )
        pd.testing.assert_series_equal(df_utc["Value"], df_cet["Value"])

    def test_input_date_formats_custom_timezone(self, connection, request):
        """User provides custom timezone for date inputs and returned time series

        Input datetime of the KIWIS API is always CET (and is not tz-aware). When a user
        defines a custom time zone-, input date is interpreted as the custom timezone,
        request is sent as CET and returned data is converted to custom timezone
        provided by the user.

        Note, there is no query option to check the timezone string for the java
        app of kisters, so we only check if string is supported by pytz.
        """
        connection = request.getfixturevalue(connection)
        df_utc_default = connection.get_timeseries_values(
            ts_id="60992042", start="20190501 14:05", end="20190501 14:10"
        )
        df_utc = connection.get_timeseries_values(
            ts_id="60992042",
            start="20190501 14:05",
            end="20190501 14:10",
            timezone="UTC",
        )
        # UTC data should be the same as CET, taken into account 2h difference
        df_cet = connection.get_timeseries_values(
            ts_id="60992042",
            start="20190501 16:05",
            end="20190501 16:10",
            timezone="CET",
        )
        pd.testing.assert_series_equal(df_utc_default["Timestamp"], df_utc["Timestamp"])
        pd.testing.assert_series_equal(
            df_cet["Timestamp"].dt.tz_convert("UTC"), df_utc["Timestamp"]
        )

    @pytest.mark.skipif(sys.version_info < (3, 9), reason="ZoneInfo is 3.9 feature")
    def test_input_datetime_custom_timezone(self, connection, request):
        """Custom timezone with datetime input support"""
        connection = request.getfixturevalue(connection)
        from datetime import datetime
        from zoneinfo import ZoneInfo

        dt_b_start = datetime(2022, 1, 1, 13, 0, tzinfo=ZoneInfo("Europe/Brussels"))
        dt_b_end = datetime(2022, 1, 1, 14, 0, tzinfo=ZoneInfo("Europe/Brussels"))
        df_brussels = connection.get_timeseries_values(
            "78073042", start=dt_b_start, end=dt_b_end, timezone="Europe/Brussels"
        )
        dt_b_naive_start = datetime(2022, 1, 1, 13, 0)
        dt_b_naive_end = datetime(2022, 1, 1, 14, 0)
        df_brussels_naive = connection.get_timeseries_values(
            "78073042",
            start=dt_b_naive_start,
            end=dt_b_naive_end,
            timezone="Europe/Brussels",
        )
        # Naive with a timezone parameter is converted to timezone
        pd.testing.assert_series_equal(
            df_brussels["Timestamp"], df_brussels_naive["Timestamp"]
        )

        dt_utc_start = datetime(2022, 1, 1, 12, 0)
        dt_utc_end = datetime(2022, 1, 1, 13, 0)
        df_utc = connection.get_timeseries_values(
            "78073042", start=dt_utc_start, end=dt_utc_end, timezone="UTC"
        )
        pd.testing.assert_series_equal(
            df_brussels["Timestamp"].dt.tz_convert("UTC"), df_utc["Timestamp"]
        )

    @pytest.mark.skipif(sys.version_info < (3, 9), reason="ZoneInfo is 3.9 feature")
    def test_overwrite_timezone(self, connection, request):
        """Check if timezone is overwritten"""
        connection = request.getfixturevalue(connection)
        df = connection.get_timeseries_values(
            ts_id="60992042", start="20190501 14:05", end="20190501 14:10"
        )
        assert df["Timestamp"].dt.tz == datetime.timezone.utc

        df = connection.get_timeseries_values(
            ts_id="60992042",
            start="20190501 14:05",
            end="20190501 14:10",
            timezone="CET",
        )
        assert isinstance(df["Timestamp"].dtype, pd.DatetimeTZDtype)
        assert df["Timestamp"].dt.tz == pytz.timezone("CET")

    def test_timezone_mixed_timezone(self, connection, request):
        """Queries resulting in mixed timezone offsets are handled without warning

        See also https://github.com/fluves/pywaterinfo/issues/67
        """
        connection = request.getfixturevalue(connection)
        df = connection.get_timeseries_values(
            "69928042",
            start="2013-03-21 00:00:00",
            end="2013-04-01 23:00:00",
            timezone="CET",
            returnfields="Timestamp,Value",
        )
        assert isinstance(df["Timestamp"].dtype, pd.DatetimeTZDtype)
        assert df["Timestamp"].dt.tz == pytz.timezone("CET")

    def test_start_end_timezone(self, connection, request):
        """pywaterinfo can handle start/end dates already containing tz info"""
        connection = request.getfixturevalue(connection)
        # string containing offset
        df_utc_string = connection.get_timeseries_values(
            ts_id="60992042",
            start="20190501 14:05:00+00:00",
            end="20190501 14:05:00+00:00",
            timezone="UTC",
        )
        assert df_utc_string.loc[0, "Timestamp"] == pd.to_datetime(
            "2019-05-01 14:05:00+00:00"
        )

        # datetime objects containing timezone info
        df_cet_zone = connection.get_timeseries_values(
            ts_id="60992042",
            start=pd.to_datetime("20190501 14:05:00").tz_localize("CET"),
            end=pd.to_datetime("20190501 14:10:00").tz_localize("CET"),
            timezone="CET",
        )
        assert df_cet_zone.loc[0, "Timestamp"] == pd.to_datetime(
            "2019-05-01 14:05:00"
        ).tz_localize("CET")

        # no assumptions are made on the tz of the input dates and the requested output,
        # CET input dates with UTC output will work and return the corresponding UTC
        # datetime of the input datetimes
        df_mixed = connection.get_timeseries_values(
            ts_id="60992042",
            start="20190501 14:05:00+02:00",
            end="20190501 14:10:00+02:00",
            timezone="UTC",
        )
        assert df_mixed.loc[0, "Timestamp"] == pd.to_datetime(
            "2019-05-01 12:05:00+00:00"
        )

    def test_invalid_timezone(self, connection, request):
        """Unknown timezone should raise error"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
            connection.get_timeseries_values(
                ts_id="60992042",
                start="20190501 14:05:00+02:00",
                end="20190501 14:10:00+02:00",
                timezone="DUMMY",
            )

    def test_return_date_format(self, connection, request):
        """Input to requested return date format should be existing on KIWIS API"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection._check_return_date_format("DUMMY")

        assert connection._check_return_date_format("yyyy-MM-dd HH:mm:ss") is None

    def test_return_fields_format(self, connection, request):
        """Input to requested returnfields should be existing on KIWIS API"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection._check_return_fields_format("DUMMY,DUMMY")


@pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
class TestTimeseriesValues:
    def test_one_of_two_ids(self, connection, request):
        """either ts_id or timeseriesgroup_id should be used"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection.get_timeseries_values(
                ts_id="78124042", timeseriesgroup_id="192900", period="P1D"
            )
        with pytest.raises(Exception):
            connection.get_timeseries_values(period="P1D")

    def test_multiple_ids(self, connection, request):
        """Call worksxpected for multiple identifiers combined in single dataframe"""
        """either ts_id or timeseriesgroup_id should be used"""
        connection = request.getfixturevalue(connection)
        df = connection.get_timeseries_values(
            ts_id="60992042,60968042", start="20190501 14:05", end="20190501 14:10"
        )
        assert set(df["ts_id"].unique()) == set(["60992042", "60968042"])

    def test_no_data(self, connection, request):
        """return empty dataframe when no data"""
        connection = request.getfixturevalue(connection)
        df = connection.get_timeseries_values(
            ts_id="60992042", start="21500501 14:05", end="21500501 14:10"
        )
        assert len(df) == 0

        # vmm_connection.clear_cache() # TODO - refactor
        df = connection.get_timeseries_values(
            ts_id="60992042,60968042", start="21500501 14:05", end="21500501 14:10"
        )
        assert len(df) == 0

    def test_datetime_conversion(self, connection, request):
        """Datetime in the returned data sets are pd.Timestamps with timezone info"""
        connection = request.getfixturevalue(connection)
        df = connection.get_timeseries_values(
            ts_id="60992042,60968042", start="20190501 14:05", end="20190501 14:10"
        )
        assert isinstance(df["Timestamp"].dtype, pd.DatetimeTZDtype)


@pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
class TestRequestKiwis:
    def test_period_check_call(self, connection, request):
        """period format checked when included"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(WaterinfoException):
            connection.request_kiwis(
                {
                    "request": "getTimeseriesValues",
                    "ts_id": "78124042",
                    "period": "PTT1D",
                }
            )

    def test_dateformat_check(self, connection, request):
        """dateformat checked when included"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(WaterinfoException) as e:
            connection.request_kiwis(
                {
                    "request": "getTimeseriesValues",
                    "ts_id": "78124042",
                    "period": "P1D",
                    "dateformat": "",
                }
            )
            assert str(e.value).contains("The requested returned datetime")

    def test_queryparam_check(self, connection, request):
        """dateformat checked when included"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(WaterinfoException):
            connection.request_kiwis(
                {"request": "getTimeseriesValues", "ts_id": "78124042", "DUMMY": ""}
            )

    def test_query_optional_fields(self, connection, request):
        """Query check on optional fields works for requests without optional fields"""
        connection = request.getfixturevalue(connection)

        # Kiwis calls without optional fields
        no_optional_fields = [
            "getColorClassifications",
            "getQualityCodes",
            "getTimeseriesReleaseStateList",
        ]
        for kiwis_request in no_optional_fields:
            assert (
                connection._check_query_parameters({"request": kiwis_request}) is None
            )


class TestRasterTimeseriesValues:

    @pytest.mark.parametrize(
        "connection",
        [
            "vmm_connection",
            "vmm_cached_connection",
            "hic_connection",
            "hic_cached_connection",
        ],
    )
    def test_get_raster_timeseries_values_invalid_provider(self, connection, request):
        """Handles if any other provider than vmm_grid is used for grid request"""

        connection = request.getfixturevalue(connection)
        with pytest.raises(
            WaterinfoException,
            match=(
                "get_raster_timeseries_values is only available for"
                " VMM grid datasource."
            ),
        ):
            connection.get_raster_timeseries_values(
                ts_id="911010",
                period="PT1H",
            )

    @pytest.mark.parametrize(
        "connection",
        [
            "vmm_grid_connection",
            "vmm_grid_cached_connection",
        ],
    )
    def test_grid_info_extra_deps(self, caplog, connection, request):
        """Test KIWIS grid request returns temp file and response"""

        # check if the logs say the The provider {provider} requires extra
        # dependencies

        with caplog.at_level(logging.INFO):
            connection = request.getfixturevalue(connection)
            assert "requires extra dependencies." in caplog.text

    @pytest.mark.parametrize(
        "connection",
        [
            "vmm_connection",
            "vmm_cached_connection",
            "hic_connection",
            "hic_cached_connection",
        ],
    )
    def test_grid_info_no_extra_deps(self, caplog, connection, request):
        """Test KIWIS grid request returns temp file and response"""

        # check if the logs say the The provider {provider} requires extra
        # dependencies

        with caplog.at_level(logging.INFO):
            connection = request.getfixturevalue(connection)
            assert "requires extra dependencies." not in caplog.text


class TestTimeseriesValueLayer:
    @pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
    def test_one_of_three(self, connection, request):
        """Should be either ts_id, bbox or timeseriesgroup_id"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection.get_timeseries_value_layer(
                ts_id="78124042", timeseriesgroup_id="192900", bbox="DUMMY"
            )

    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_hic(self, connection, request):
        connection = request.getfixturevalue(connection)
        df = connection.get_timeseries_value_layer(timeseriesgroup_id="156207")
        assert "ts_id" in df.columns


class TestGroupList:
    @pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
    def test_group_type(self, connection, request):
        """Error from the KIWIS when nothing returned

        To be consistent with other sections, should be an empty dataframe.
        As this function is probably not used in returning tasks, keeping as such.
        """
        connection = request.getfixturevalue(connection)
        with pytest.raises(Exception):
            connection.get_group_list(group_type="DUMMY")

    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_hic(self, connection, request):
        connection = request.getfixturevalue(connection)
        df = connection.get_group_list()
        assert "group_id" in df.columns


class TestTimeseriesList:
    @pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
    def test_no_data(self, connection, request):
        """Empty dataframe when no data is returned"""
        connection = request.getfixturevalue(connection)
        assert connection.get_timeseries_list(station_no="DUMMY").equals(
            pd.DataFrame([])
        )

    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_hic(self, connection, request):
        """"""
        connection = request.getfixturevalue(connection)
        df = connection.get_timeseries_list(station_no="plu03a-1066")
        assert "station_no" in df.columns


class TestEnsembleTimeSeries:
    @pytest.mark.parametrize("connection", ["vmm_connection", "vmm_cached_connection"])
    def test_not_available_apart_from_hic(self, connection, request):
        """If provider is not HIC, WaterinfoException should be raised"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(WaterinfoException) as excinfo:
            connection.get_ensemble_timeseries_values()
            assert str(excinfo.value) == "Ensemble data only available for HIC."

    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"ts_id": "84017010,84327010,84150010"},
            {
                "ts_path": "Maastricht/SINT-WL1-1060/Ncatch"
                "_voorspeld/Cmd.Ensemble.Binary.KT-det.O"
                ","
                "Helkijn/bos05m-1066/Ncatch"
                "_voorspeld/Cmd.Ensemble.Binary.KT-det.O"
            },
        ],
    )
    def test_commaseperated_ids_or_paths(self, connection, kwargs, request):
        """Allow commaseperated identifiers until implemented"""
        conn = request.getfixturevalue(connection)

        data = conn.get_ensemble_timeseries_values(
            start="2025-06-01T00:00:00Z", end="2025-06-01T12:00:00Z", **kwargs
        )
        assert isinstance(data, pd.DataFrame)
        assert "ensembledate" in data.columns
        assert "ensembledispatchinfo" in data.columns
        assert not data.empty

    @pytest.mark.parametrize(
        "ts_id",
        [84021010, 84019010],
    )
    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_valid_request_ts_id_int(self, ts_id, connection, request):
        """For valid cases, a pd.dataframe with ensemble members should be returned"""
        conn = request.getfixturevalue(connection)

        data = conn.get_ensemble_timeseries_values(
            start="2025-06-01T00:00:00Z",
            end="2025-06-01T12:00:00Z",
            ts_id=ts_id,
        )
        assert isinstance(data, pd.DataFrame)
        assert "ensembledate" in data.columns
        assert "ensembledispatchinfo" in data.columns
        assert not data.empty

    @pytest.mark.parametrize(
        "ts_path",
        [
            "Aarschot/dem02a-1066/Q_voorspeld/Cmd.Ensemble.Binary.KT-det.O",
            "Aarschot/dem02a-1066/H_voorspeld/Cmd.Ensemble.Binary.KT-Perc.Abs.O",
        ],
    )
    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_valid_request_ts_path(self, ts_path, connection, request):
        """For valid cases, a pd.dataframe with ensemble members should be returned"""
        conn = request.getfixturevalue(connection)

        data = conn.get_ensemble_timeseries_values(
            start="2025-06-01T00:00:00Z",
            end="2025-06-01T12:00:00Z",
            ts_path=ts_path,
        )
        assert isinstance(data, pd.DataFrame)
        assert "ensembledate" in data.columns
        assert "ensembledispatchinfo" in data.columns
        assert not data.empty

    @pytest.mark.parametrize(
        "tz",
        ["Europe/Brussels", "CET", "EST", "Greenwich"],
    )
    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_timezone_provided(self, tz, connection, request):
        """If timezone is overwritten, data should have timezone information"""
        conn = request.getfixturevalue(connection)
        data = conn.get_ensemble_timeseries_values(
            start="2025-06-01T00:00:00",
            end="2025-06-01T12:00:00",
            ts_id="84021010",
            timezone=tz,
        )

        assert isinstance(data, pd.DataFrame)
        assert data["Timestamp"].dt.tz.zone == tz
        assert not data.empty

    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_timezone_not_provided(self, connection, request):
        """If timezone is not provided, data should timezone of UTC."""
        conn = request.getfixturevalue(connection)
        data = conn.get_ensemble_timeseries_values(
            start="2025-06-01T00:00:00",
            end="2025-06-01T12:00:00",
            ts_id="84021010",
        )

        assert isinstance(data, pd.DataFrame)
        assert data["Timestamp"].dt.tz == datetime.timezone.utc

    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_cannot_have_two_identifiers(self, connection, request):
        """Do not allow multiple identifiers"""
        conn = request.getfixturevalue(connection)
        with pytest.raises(WaterinfoException) as excinfo:
            conn.get_ensemble_timeseries_values(
                ts_id="tsid1",
                ts_path="data/path",
                start="2025-06-01T00:00:00Z",
                end="2025-06-01T12:00:00Z",
            )
        assert str(excinfo.value) == (
            "A combination of ts_id and ts_path is not possible, use one"
        )

    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_no_identifier(self, connection, request):
        """If no identifier is provided, WaterinfoException should be raised"""
        conn = request.getfixturevalue(connection)
        with pytest.raises(WaterinfoException) as excinfo:
            conn.get_ensemble_timeseries_values(
                start="2025-06-01T00:00:00Z",
                end="2025-06-01T12:00:00Z",
            )
            assert str(excinfo.value) == ("Either ts_id or ts_path is required.")

    @pytest.mark.parametrize("connection", ["hic_connection", "hic_cached_connection"])
    def test_no_date_or_period(self, connection, request):
        """If no date or period is provided, NotImplementedError should be raised"""
        conn = request.getfixturevalue(connection)
        with pytest.raises(NotImplementedError) as excinfo:
            conn.get_ensemble_timeseries_values(
                ts_id="84021010",
            )
            assert str(excinfo.value) == (
                "Currently, pywaterinfo doesn't support calling "
                "`get_ensemble_timeseries_values` without any time information."
            )


class TestGridRasterFile:

    @pytest.mark.parametrize(
        "connection",
        [
            "vmm_grid_connection",
            "vmm_grid_cached_connection",
        ],
    )
    def test_grid_raster_file_valid_provider(self, connection, request):
        """Test KIWIS grid raster file request"""
        connection = request.getfixturevalue(connection)
        with pytest.raises(
            NotImplementedError, match="Binary io needs to be implemented."
        ):
            connection.get_raster_timeseries_values(
                ts_id="911010",
                period="PT1H",
            )

    @pytest.mark.parametrize(
        "connection",
        [
            "vmm_connection",
            "vmm_cached_connection",
            "hic_connection",
            "hic_cached_connection",
        ],
    )
    def test_grid_raster_file_invalid_provider(self, connection, request):
        """Test KIWIS grid raster file request"""
        connection = request.getfixturevalue(connection)

        with pytest.raises(
            WaterinfoException, match="only available from the VMM grid datasource."
        ):
            connection.get_raster_timeseries_values(
                ts_id="911010",
                period="PT1H",
            )
