import numpy as np
import geopandas as gpd
import xarray as xr

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.25, rc={"lines.linewidth": 2})

# shps
shp_drainages = gpd.read_file("./data/raw/vectorial/vertientes.shp").to_crs({"init": "epsg:4326"})
shp_SA = gpd.read_file("./data/raw/vectorial/Sudamérica.shp").to_crs({"init": "epsg:4326"})
shp_lks = gpd.read_file("./data/raw/vectorial/lago_titicaca_sideteva_puno.shp").to_crs({"init": "epsg:4326"})

# gridded
pisco_trend = xr.open_dataset("./data/processed/pisco_data_trends.nc")


#
plt.rcParams['hatch.linewidth'] = .15
plt.rcParams['hatch.color'] = "black"

fig, ax0 = plt.subplots(1, 1, figsize = (3, 7), dpi = 200)

var = "ai"

nc_data = pisco_trend[var + "_slope"]
max_value = np.round([np.nanmax(np.abs(nc_data.values))], 1).max()
plot_b = nc_data.plot(ax = ax0, add_colorbar=False, cmap="PiYG_r", levels = np.arange(-max_value, max_value+.1, .1))
pisco_trend[var + "_pvalue"].plot.contourf(ax = ax0, hatches=["","xxx"], levels = [0, 0.5], alpha=0, add_colorbar=False)

axin = inset_axes(ax0, width='5%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax0.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('', labelpad=-43, size = 9)
cb.ax.tick_params(labelsize = 7, length=1, width=.5, pad = 0)

shp_drainages.geometry.boundary.plot(ax = ax0, edgecolor = "gray", linewidth = 1, alpha=.25)
shp_SA.geometry.boundary.plot(ax = ax0, edgecolor = "gray", linewidth = 1)
shp_lks.plot(ax = ax0, edgecolor = "deepskyblue", color = "deepskyblue")

ax0.set_ylim(-18.5, 0.5)
ax0.set_xlim(-81.75, -68)
ax0.set_ylabel("")
ax0.set_xlabel("")
ax0.set_title("")
ax0.xaxis.set_tick_params(labelsize = 7, pad = -3)
ax0.yaxis.set_tick_params(labelsize = 7, pad = -3)
ax0.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('./data/output/figs/02_ai_trend.png',
            bbox_inches='tight',pad_inches = 0, dpi = 200)
plt.close()


##

plt.rcParams['hatch.linewidth'] = .15
plt.rcParams['hatch.color'] = "black"

fig, (ax0, ax1) = plt.subplots(1, 2, figsize = (8, 5), dpi = 200)

var = "pet"

nc_data = pisco_trend[var + "_slope"]
max_value = np.round([np.nanmax(np.abs(nc_data.values))], 1).max()
plot_b = nc_data.plot(ax = ax0, add_colorbar=False, cmap="PiYG_r", levels = np.arange(-max_value, max_value+.1, .1))
pisco_trend[var + "_pvalue"].plot.contourf(ax = ax0, hatches=["","XXXX"], levels = [0, 0.5], alpha=0, add_colorbar=False)

axin = inset_axes(ax0, width='5%', height='35%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax0.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('PET (mm/década)', labelpad=-43, size = 8)
cb.ax.tick_params(labelsize = 8, length=1, width=.5, pad = 0)

shp_drainages.geometry.boundary.plot(ax = ax0, edgecolor = "gray", linewidth = .75, alpha=.25)
shp_SA.geometry.boundary.plot(ax = ax0, edgecolor = "gray", linewidth = .75)
shp_lks.plot(ax = ax0, edgecolor = "deepskyblue", color = "deepskyblue")

#ax0.legend(*g.legend_elements(),)
#ax0.legend(*g1.legend_elements(),)
ax0.set_ylim(-18.5, 0.5)
ax0.set_xlim(-81.75, -68)
ax0.set_ylabel("")
ax0.set_xlabel("")
ax0.set_title("")
ax0.xaxis.set_tick_params(labelsize = 7, pad = -3)
ax0.yaxis.set_tick_params(labelsize = 7, pad = -3)
ax0.grid(True, linestyle='--', color = "black", alpha = 0.1)

var = "p"

nc_data = pisco_trend[var + "_slope"]
max_value = np.round([np.nanmax(np.abs(nc_data.values))], 1).max()
plot_b = nc_data.plot(ax = ax1, add_colorbar=False, cmap="PiYG_r", levels = np.arange(-max_value, max_value+.1, .1))
pisco_trend[var + "_pvalue"].plot.contourf(ax = ax1, hatches=["","XXXX"], levels = [0, 0.5], alpha=0, add_colorbar=False)

axin = inset_axes(ax1, width='5%', height='35%', loc = 'lower left', bbox_to_anchor = (0.03, 0.025, 1 ,1), bbox_transform = ax1.transAxes)
cb = plt.colorbar(plot_b, cax=axin, orientation = "vertical", aspect = 5)
cb.ax.set_ylabel('P (mm/década)', labelpad=-47, size = 8)
cb.ax.tick_params(labelsize = 8, length=1, width=.5, pad = 0)

shp_drainages.geometry.boundary.plot(ax = ax1, edgecolor = "gray", linewidth = .75, alpha=.25)
shp_SA.geometry.boundary.plot(ax = ax1, edgecolor = "gray", linewidth = .75)
shp_lks.plot(ax = ax1, edgecolor = "deepskyblue", color = "deepskyblue")
#ax1.legend(*g.legend_elements(),)
#ax1.legend(*g1.legend_elements(),)

ax1.set_ylim(-18.5, 0.5)
ax1.set_xlim(-81.75, -68)
ax1.set_ylabel("")
ax1.set_xlabel("")
ax1.set_title("")
ax1.xaxis.set_tick_params(labelsize = 7, pad = -3)
ax1.yaxis.set_tick_params(labelsize = 7, pad = -3)
ax1.grid(True, linestyle='--', color = "black", alpha = 0.1)


#plt.subplots_adjust(wspace=0.0001, hspace=0.05)
plt.savefig('./data/output/figs/03_pet_p_trend.png',
            bbox_inches='tight',pad_inches = 0, dpi = 230)
plt.close()
