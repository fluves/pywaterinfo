import time

from pywaterinfo import Waterinfo


def test_cache_vmm(vmm_connection):
    """Second call of the same request is retrieved from cache for VMM requests."""
    vmm_connection.clear_cache()
    data, res = vmm_connection.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache
    data, res = vmm_connection.request_kiwis({"request": "getRequestInfo"})
    assert res.from_cache


def test_cache_hic(hic_connection):
    """Second call of the same request is retrieved from cache for HIC requests."""
    hic_connection.clear_cache()
    data, res = hic_connection.request_kiwis(
        query={"request": "getTimeseriesValueLayer", "timeseriesgroup_id": "156207"}
    )
    assert not res.from_cache
    data, res = hic_connection.request_kiwis(
        query={"request": "getTimeseriesValueLayer", "timeseriesgroup_id": "156207"}
    )
    assert res.from_cache


{"request": "getTimeseriesValueLayer", "timeseriesgroup_id": "156207"}


def test_clear_cache(vmm_connection):
    """Cache is cleared."""
    vmm_connection.clear_cache()
    data, res = vmm_connection.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache
    vmm_connection.clear_cache()
    data, res = vmm_connection.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache


def test_cache_retention_between_sessions():
    """Requests are chached in between two sessions."""
    vmm = Waterinfo("vmm")
    vmm.clear_cache()
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache

    # New session reuses the same database
    vmm = Waterinfo("vmm")
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert res.from_cache


def test_cache_retention(patch_retention):
    """Request is not from cache after expiration date.

    Uses monkeypatch version of the CACHE_RETENTION timing for unit testing.

    Notes
    -----
    See requests-cache.readthedocs.io/en/stable/user_guide/headers.html,
    conditional requests are automatically sent for any servers that support them. Once
    a cached response expires, it will only be updated if the
    remote content has changed. Hence, we check here for expiration first, remove the
    expired cache and check for `from_cache` in a new request.
    """
    vmm = Waterinfo("vmm")
    vmm.clear_cache()
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache

    time.sleep(1)
    vmm = Waterinfo("vmm")
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert res.is_expired

    vmm._request.remove_expired_responses()
    _, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache
