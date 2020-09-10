import numpy as np
import geopandas as gpd
import xarray as xr
import pymannkendall as mk
import rioxarray
from multipy.fdr import lsu

exec(open("./src/MK_trend.py").read())

shp_peru_no_lake = gpd.read_file("./data/raw/vectorial/Peru_no_lake.shp").to_crs({"init": "epsg:4326"})

pisco = xr.open_dataset("./data/processed/pisco_data.nc")

gridded_trend = xr.Dataset({})
grid_data = pisco["p"].rio.set_crs(shp_peru_no_lake.crs)
grid_data = grid_data.rio.clip(shp_peru_no_lake.geometry, grid_data.rio.crs)
gridded_trend["p"] = grid_data

for var in list(pisco._variables.keys())[3:]:

    var_data = pisco[var]
    var_data = var_data.rio.set_crs(shp_peru_no_lake.crs)
    var_data = var_data.rio.clip(shp_peru_no_lake.geometry, var_data.rio.crs)

    gridded_trend[var + "_slope"] = (('latitude', 'longitude'), np.apply_along_axis(slope_trend, 0, var_data))
    gridded_trend[var + "_slope"] = gridded_trend[var + "_slope"]*10
    gridded_trend[var + "_pvalue"] = (('latitude', 'longitude'), np.apply_along_axis(pvalue_trend, 0, var_data))
    gridded_trend[var + "_pvalue"].values = (lsu(pvals=gridded_trend[var + "_pvalue"].values.ravel()) + 0).reshape(183, 126)


gridded_trend = gridded_trend.drop_vars("p")
gridded_trend.to_netcdf("./data/processed/pisco_data_trends.nc")


