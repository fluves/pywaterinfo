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
    data, res = hic_connection.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache
    data, res = hic_connection.request_kiwis({"request": "getRequestInfo"})
    assert res.from_cache


def test_clear_cache(vmm_connection):
    """Cache is cleared."""
    vmm_connection.clear_cache()
    data, res = vmm_connection.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache
    vmm_connection.clear_cache()
    data, res = vmm_connection.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache


def test_cache_retention(patch_retention):
    """Request is not from cache after expiration date.

    Uses monkeypatch version of the CACHE_RETENTION timing for unit testing.
    """
    vmm = Waterinfo("vmm")
    data, res = vmm.request_kiwis({"request": "getRequestInfo"})

    time.sleep(2)
    data, res = vmm.request_kiwis({"request": "getRequestInfo"})
    assert not res.from_cache
