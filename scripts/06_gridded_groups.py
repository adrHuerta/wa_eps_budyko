import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd
import rioxarray
import pickle

shp_obs = gpd.read_file("./data/raw/Caudal/PEQ_1981-2020_subcuencas_GR2M_Peru_SHP/Subbasins_GR2M_Peru.shp")
pisco_grid = xr.open_dataset("./data/processed/pisco_data.nc").p.isel(time=0)
pisco_grid = pisco_grid.rio.set_crs("epsg:4326")

shp_order = sorted(shp_obs.Region.unique())

for i in range(len(shp_order)):
    shp_obs.loc[(shp_obs.Region == shp_order[i]), "Region"] = i + 1

gridded_groups = []
for group in shp_obs.Region.unique():
    subx = shp_obs.loc[shp_obs.Region == group]
    grid_value = pisco_grid.rio.clip(subx.geometry, drop=False)
    grid_value.values[~np.isnan(grid_value.values)] = int(subx.Region.unique())
    grid_value = grid_value.fillna(0)
    gridded_groups.append(grid_value)

gridded_groups = (gridded_groups[0] + gridded_groups[1] + gridded_groups[2] + gridded_groups[3] +
                  gridded_groups[4] +
                  gridded_groups[5] + gridded_groups[6] + gridded_groups[7] + gridded_groups[8] +
                  gridded_groups[9] + gridded_groups[10] + gridded_groups[11] + gridded_groups[12] +
                  gridded_groups[13])

gridded_groups.values[gridded_groups.values == 0] = np.nan
gridded_groups.to_dataset(name="gridded_groups").drop(["spatial_ref", "time"]).\
    to_netcdf("./data/processed/budyko_groups2.nc")


"""
shp_obs = pickle.load(open("./data/processed/qobs.pkl","rb"))["clim"]
shp_drainages = gpd.read_file("./data/raw/vectorial/vertientes.shp").to_crs({"init": "epsg:4326"})
shp_drainages.columns = ['OBJECTID', 'Vertiente', 'COD_GDB', 'COD_UNICO', 'SHAPE_Leng', 'SHAPE_Area', 'geometry']

import matplotlib.pyplot as plt

# testing if shp_drainages share with shp_obs

fig, ax = plt.subplots()
shp_obs.loc[shp_obs.Vertiente == "Atlántico"].iloc[[0,1,10,11]].plot(ax=ax)
shp_drainages[shp_drainages.Vertiente == "Región Hidrográfica del Amazonas"].plot(ax=ax,cmap="OrRd")

atlantico = gpd.GeoDataFrame(
    pd.concat([shp_drainages.loc[shp_drainages.Vertiente == "Región Hidrográfica del Amazonas"],
               shp_obs.loc[shp_obs.Vertiente == "Atlántico"].iloc[[0,1,10,11]]]),
    crs=shp_drainages.crs)
atlantico['new_column'] = 0
atlantico = atlantico.dissolve(by='new_column')


fig, ax = plt.subplots()
shp_obs.loc[shp_obs.Vertiente == "Pacífico"].iloc[[2,3]].plot(ax=ax)
shp_drainages.loc[shp_drainages.Vertiente == "Región Hidrografica del Pacífico"].plot(ax=ax,cmap="OrRd")

pacifico = gpd.GeoDataFrame(
    pd.concat([shp_drainages.loc[shp_drainages.Vertiente == "Región Hidrografica del Pacífico"],
               shp_obs.loc[shp_obs.Vertiente == "Pacífico"].iloc[[2,3]]]),
    crs=shp_drainages.crs)
pacifico['new_column'] = 0
pacifico = pacifico.dissolve(by='new_column')

fig, ax = plt.subplots()
shp_drainages.loc[shp_drainages.Vertiente == "Región Hidrográfica del Titicaca"].plot(ax=ax)
shp_obs.loc[shp_obs.Vertiente == "Titicaca"].plot(ax=ax)

titicaca = gpd.GeoDataFrame(
    pd.concat([shp_drainages.loc[shp_drainages.Vertiente == "Región Hidrográfica del Titicaca"],
               shp_obs.loc[shp_obs.Vertiente == "Titicaca"]]),
    crs=shp_drainages.crs)
titicaca['new_column'] = 0
titicaca = titicaca.dissolve(by='new_column')

shp_drainages = gpd.GeoDataFrame(
    pd.concat([atlantico, pacifico, titicaca]),
    crs = shp_drainages.crs)

pisco_grid = xr.open_dataset("./data/processed/pisco_data.nc").sel(time=slice('2000-01-01', '2016-12-31')).p.isel(time=0)
pisco_grid = pisco_grid.rio.set_crs("epsg:4326")

shp_order = ["Región Hidrográfica del Amazonas", "Región Hidrografica del Pacífico", "Región Hidrográfica del Titicaca"]

for i in range(len(shp_order)):
    shp_drainages.loc[(shp_drainages.Vertiente == shp_order[i]), "OBJECTID"] = i + 1

gridded_groups = []
for group in shp_drainages.Vertiente:
    subx = shp_drainages.loc[shp_drainages.Vertiente == group]
    grid_value = pisco_grid.rio.clip(subx.geometry, drop=False)
    grid_value.values[~np.isnan(grid_value.values)] = int(subx.OBJECTID.values)
    grid_value = grid_value.fillna(0)
    gridded_groups.append(grid_value)

gridded_groups = (gridded_groups[0] + gridded_groups[1] + gridded_groups[2])
gridded_groups.values[gridded_groups.values == 0] = np.nan
gridded_groups.to_dataset(name="gridded_groups").drop(["spatial_ref", "time"]).\
    to_netcdf("./data/processed/budyko_groups.nc")
"""
