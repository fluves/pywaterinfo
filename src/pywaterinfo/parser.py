import numpy as np
import pandas as pd
import xarray as xr


def parse_waterinfo_hdf5(h5f):
    """Parse Waterinfo HDF5 radar data structure into an xarray Dataset.

    This function extracts precipitation radar data from Waterinfo.be HDF5
    files, which have a specific structure with spatial information in the
    'where' group attributes and time-series data in the 'dataset1' group.

    Parameters
    ----------
    h5f : h5py.File or io.BytesIO
        Opened HDF5 file object or file-like object containing Waterinfo radar
        data.

    Returns
    -------
    xr.Dataset
        Dataset containing precipitation data with dimensions (time, y, x) and
        the 'precipitation' variable.
    """

    # Extract spatial information from 'where' attributes
    where_attrs = h5f["where"].attrs

    # Grid parameters
    xsize = where_attrs["xsize"]  # 900
    ysize = where_attrs["ysize"]  # 780
    xscale = where_attrs["xscale"]  # 500.0 (meter grid resolution)
    yscale = where_attrs["yscale"]  # 500.0 (meter grid resolution)

    # Projection definition
    projdef = (
        where_attrs["projdef"].decode("utf-8")
        if isinstance(where_attrs["projdef"], bytes)
        else where_attrs["projdef"]
    )

    # Create coordinate arrays in projected coordinates
    # The origin seems to be at (LL_lon, LL_lat) in projected coordinates
    x_coords = np.arange(0, xsize) * xscale + where_attrs["LL_lon"]
    y_coords = np.arange(0, ysize) * yscale + where_attrs["LL_lat"]

    # Extract time information from data groups
    dataset1 = h5f["dataset1"]
    data_groups = sorted(
        [key for key in dataset1.keys() if key.startswith("data")],
        key=lambda x: int(x[4:]),
    )  # Sort by number after 'data'

    print(f"Found {len(data_groups)} timesteps")

    # Extract timestamps from 'what' group
    what_attrs = h5f["what"].attrs
    base_date = (
        what_attrs["date"].decode("utf-8")
        if isinstance(what_attrs["date"], bytes)
        else what_attrs["date"]
    )
    base_time = (
        what_attrs["time"].decode("utf-8")
        if isinstance(what_attrs["time"], bytes)
        else what_attrs["time"]
    )

    print(f"Base date/time: {base_date} {base_time}")

    # Parse base datetime
    base_dt = pd.to_datetime(f"{base_date} {base_time}", format="%Y%m%d %H%M%S")

    # Create timesteps (assuming 10-minute intervals for radar data)
    timesteps = [
        base_dt + pd.Timedelta(minutes=10 * i) for i in range(len(data_groups))
    ]

    # Read all data arrays and replace -2 with np.nan
    data_arrays = []
    for i, data_group_name in enumerate(data_groups):
        data_group = dataset1[data_group_name]
        data_array = data_group["data"][:]

        # Replace -2 (no_data) with np.nan
        data_array = data_array.astype(np.float64)  # Convert to float to support NaN
        data_array[data_array == -2] = np.nan

        data_arrays.append(data_array)

    # Stack into 3D array (time, y, x)
    data_3d = np.stack(data_arrays, axis=0)

    # Create xarray Dataset
    ds = xr.Dataset(
        {"precipitation": (["time", "y", "x"], data_3d)},
        coords={"time": timesteps, "x": x_coords, "y": y_coords},
        attrs={
            "crs": projdef,
            "projection": projdef,
            "description": "Precipitation radar data from Waterinfo.be",
            "grid_resolution_x": xscale,
            "grid_resolution_y": yscale,
            "xsize": xsize,
            "ysize": ysize,
            "nodata_value": np.nan,  # Mark that we've handled no_data values
        },
    )

    return ds
