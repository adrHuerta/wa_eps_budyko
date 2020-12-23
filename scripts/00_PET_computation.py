import xarray as xr
import numpy as np
from pandas import date_range as pd_date_range

# PET function
exec(open("./src/hargreaves_samani.py").read())

# getting data
piscotx = xr.open_dataset("./data/raw/PISCO/PISCOdtx_v1.1.nc")
piscotn = xr.open_dataset("./data/raw/PISCO/PISCOdtn_v1.1.nc")

# building lat grid
pisco_lat = xr.DataArray(np.tile(piscotx["latitude"].values, (145, 1)).transpose(),
                         coords=[piscotx["latitude"].values, piscotx["longitude"].values],
                         dims=["latitude", "longitude"])

# getting time values as Julian day
"""
# as gridded, not efficient
[np.full((145, 202), i) for i in dates]
np.stack([np.full((145, 202), 1), np.full((145, 202), 2), np.full((145, 202), 3)], axis=2).shape
"""
dates = pd_date_range('1981-01-01', "2016-12-31", freq='D')
dates = np.array([int(i.strftime("%j")) for i in dates])


# computing PET

for year in range(1981, 2017):

    dates = pd_date_range(str(year) + '-01-01', str(year) + "-12-31", freq='D')
    dates = np.array([int(i.strftime("%j")) for i in dates])

    xr.apply_ufunc(hargreaves_samani,
                   piscotx.tx.loc[str(year) + '-01-01':str(year) + "-12-31"],
                   piscotn.tn.loc[str(year) + '-01-01':str(year) + "-12-31"],
                   dates,
                   pisco_lat,
                   vectorize=True,
                   input_core_dims=[["time"], ["time"], ["time"], []],
                   output_core_dims=[["time"]],
                   output_dtypes=['float64']).\
        transpose("time", "latitude", "longitude").\
        to_dataset(name="pet").\
        to_netcdf("./data/raw/PET/" + str(year) + ".nc")