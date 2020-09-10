import pandas as pd
import geopandas as gpd
import xarray as xr
import rioxarray

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.25, rc={"lines.linewidth": 2})

# shps
shp_peru = gpd.read_file("./data/raw/vectorial/Sudamérica.shp").to_crs({"init": "epsg:4326"}).iloc[11:12]
shp_peru_no_lake = gpd.read_file("./data/raw/vectorial/Peru_no_lake.shp").to_crs({"init": "epsg:4326"})
shp_drainages = gpd.read_file("./data/raw/vectorial/vertientes.shp").to_crs({"init": "epsg:4326"})
shp_dep = gpd.read_file("./data/raw/vectorial/DEPARTAMENTOS.shp").to_crs({"init": "epsg:4326"})
shp_SA = gpd.read_file("./data/raw/vectorial/Sudamérica.shp").to_crs({"init": "epsg:4326"})
shp_lks = gpd.read_file("./data/raw/vectorial/lago_titicaca_sideteva_puno.shp").to_crs({"init": "epsg:4326"})

# gridded
pisco_p = xr.open_dataset("/home/adrian/Documents/wa_budyko_datasets/netcdf/P/PISCOpd.nc").\
    rename({"z":"time"}).\
    isel(time = 0)

pisco_tx = xr.open_dataset("/home/adrian/Documents/wa_budyko_datasets/netcdf/T/PISCOdtx_v1.1.nc").\
    isel(time = 0)

# figure
fig, (ax0, ax1) = plt.subplots(1, 2, figsize = (8, 5), dpi = 200)

to_plt = pisco_p.p.rio.set_crs(shp_peru_no_lake.crs)
plot_b = to_plt.rio.clip(shp_peru_no_lake.geometry, to_plt.rio.crs).plot(ax = ax0, cmap='viridis_r',
                                                                           add_colorbar=False)
axin = inset_axes(ax0, width='5%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax0.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('Precipitación (mm)', labelpad=-43, size = 9)
cb.ax.tick_params(labelsize = 8)

shp_drainages.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .75)
shp_SA.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .25)
shp_dep.geometry.boundary.plot(ax = ax0, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax0, edgecolor = "deepskyblue", color = "deepskyblue")

ax0.set_ylim(-18.5, 0.5)
ax0.set_xlim(-81.75, -68)
ax0.set_ylabel("")
ax0.set_xlabel("")
ax0.set_title("")
ax0.xaxis.set_tick_params(labelsize = 7, pad = -3)
ax0.yaxis.set_tick_params(labelsize = 7, pad = -3)
ax0.grid(True, linestyle='--', color = "black", alpha = 0.1)

to_plt = pisco_tx.tx.rio.set_crs(shp_peru_no_lake.crs)
plot_b = to_plt.rio.clip(shp_peru_no_lake.geometry, to_plt.rio.crs).plot(ax = ax1, cmap = "viridis",
                                                                           add_colorbar=False)
axin = inset_axes(ax1, width='5%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax1.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('Temp. máxima (°C)', labelpad=-38, size = 8)
cb.ax.tick_params(labelsize = 8)

shp_drainages.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .75)
shp_SA.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .25)
shp_dep.geometry.boundary.plot(ax = ax1, edgecolor = "black", linewidth = .25)
shp_lks.plot(ax = ax1, edgecolor = "deepskyblue", color = "deepskyblue")

ax1.set_ylim(-18.5, 0.5)
ax1.set_xlim(-81.75, -68)
ax1.set_ylabel("")
ax1.set_xlabel("")
ax1.set_title("")
ax1.xaxis.set_tick_params(labelsize = 7, pad = -3)
ax1.yaxis.set_tick_params(labelsize = 7, pad = -3)

ax1.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('./data/output/figs/00_study_area_and_gridded_data.png',
            bbox_inches='tight',pad_inches = 0, dpi = 200)

plt.close()