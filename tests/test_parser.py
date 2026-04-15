import h5py
import numpy as np

from pywaterinfo.parser import parse_waterinfo_hdf5


def test_parse_waterinfo_hdf5_expected_model(mock_vmm_grid_hdf5_response):
    """Verify parsing of attrs, dims, dtypes and values correctly from hdf5 file

    Parameters
    ----------
    mock_vmm_grid_hdf5_response : BytesIO
        Mock HDF5 response from VMM grid API for testing.

    """

    expected_attrs_keys = (
        "projdef",
        "xscale",
        "yscale",
        "xsize",
        "ysize",
    )

    expected_dimensions = ("time", "y", "x")

    expected_value_dtype = np.float32

    with h5py.File(mock_vmm_grid_hdf5_response, "r") as f:
        result = parse_waterinfo_hdf5(f, nan_value=-2)

    assert "value" in result.data_vars
    assert result.data_vars["value"].dims == expected_dimensions
    assert result.data_vars["value"].dtype == expected_value_dtype
    assert set(result.attrs.keys()) == set(expected_attrs_keys)
