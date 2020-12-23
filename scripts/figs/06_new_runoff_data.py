import xarray as xr
import pandas as pd
import geopandas as gpd
import numpy as np
import pickle
import glob
import itertools

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.1, rc={"lines.linewidth": 2})

# groups
shp_obs = gpd.read_file("./data/raw/Caudal/PEQ_1981-2020_subcuencas_GR2M_Peru_SHP/Subbasins_GR2M_Peru.shp")
shp_obs = shp_obs.dissolve(by="Region")
budyko_groups = xr.open_dataset("./data/processed/budyko_groups.nc").gridded_groups

fig, ax = plt.subplots(figsize = (4, 5), dpi = 200)
plot_a = budyko_groups.plot(ax = ax, cmap = "jet", levels=[1,2,3,4,5,6,7,8,9,10,11,12,13,14, 15], add_colorbar=False)
axin = inset_axes(ax, width='8%', height='40%', loc = 'lower left', bbox_to_anchor = (0.05, 0.025, 1 ,1), bbox_transform = ax.transAxes)
cb = plt.colorbar(plot_a, cax=axin, orientation = "vertical", aspect = 5, ticks = np.arange(1.5, 15, 1))
cb.ax.set_yticklabels([1,2,3,4,5,6,7,8,9,10,11,12,13,14])
cb.ax.set_ylabel('', labelpad=-43, size = 9)
cb.ax.tick_params(labelsize = 7, length=1, width=.5, pad = 0)

ax.set_ylim(-18.5, 1.5)
ax.set_xlim(-81.75, -68)
ax.set_ylabel("")
ax.set_xlabel("")
ax.set_title("")
ax.xaxis.set_tick_params(labelsize = 7, pad = -3)
ax.yaxis.set_tick_params(labelsize = 7, pad = -3)
ax.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('./data/output/figs/06_spatial_clusters.png',
            bbox_inches='tight',pad_inches = 0.1, dpi = 125)
plt.close()


# omgega
omega_value = sorted(glob.glob("./data/processed/runoff/omega_*.pkl"))
omega_value = [pickle.load(open(i,"rb")) for i in omega_value]

a1 = [list(omega_value[i][0]) for i in range(len(omega_value))]
a2 = [list(omega_value[i][1]) for i in range(len(omega_value))]
a3 = [list(omega_value[i][2]) for i in range(len(omega_value))]
a4 = [list(omega_value[i][3]) for i in range(len(omega_value))]
a5 = [list(omega_value[i][4]) for i in range(len(omega_value))]
a6 = [list(omega_value[i][5]) for i in range(len(omega_value))]
a7 = [list(omega_value[i][6]) for i in range(len(omega_value))]
a8 = [list(omega_value[i][7]) for i in range(len(omega_value))]
a9 = [list(omega_value[i][8]) for i in range(len(omega_value))]
a10 = [list(omega_value[i][9]) for i in range(len(omega_value))]
a11 = [list(omega_value[i][10]) for i in range(len(omega_value))]
a12 = [list(omega_value[i][11]) for i in range(len(omega_value))]
a13 = [list(omega_value[i][12]) for i in range(len(omega_value))]
a14 = [list(omega_value[i][13]) for i in range(len(omega_value))]

a1 = list(itertools.chain.from_iterable(a1))
a2 = list(itertools.chain.from_iterable(a2))
a3 = list(itertools.chain.from_iterable(a3))
a4 = list(itertools.chain.from_iterable(a4))
a5 = list(itertools.chain.from_iterable(a5))
a6 = list(itertools.chain.from_iterable(a6))
a7 = list(itertools.chain.from_iterable(a7))
a8 = list(itertools.chain.from_iterable(a8))
a9 = list(itertools.chain.from_iterable(a9))
a10 = list(itertools.chain.from_iterable(a10))
a11 = list(itertools.chain.from_iterable(a11))
a12 = list(itertools.chain.from_iterable(a12))
a13 = list(itertools.chain.from_iterable(a13))
a14 = list(itertools.chain.from_iterable(a14))

fig, axes = plt.subplots(3, 5, figsize = (8, 4), constrained_layout=True, dpi = 120)

for ((i, ax), obj, i_area) in zip(enumerate(fig.axes), [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14], ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]):
    sns.histplot(pd.Series(obj), discrete=True, ax = ax, stat="density")
    ax.set_title(r"$\bf{" + str(i_area) + "}$")
    ax.set_ylim(0, 1)
    ax.set_xlim(1.1, 10.9)
    ax.set_ylabel("")

for ax in axes.flat:
    ax.xaxis.set_tick_params(labelsize=7, pad=-3)
    ax.yaxis.set_tick_params(labelsize=7, pad=-3)

fig.delaxes(axes[2][4])

plt.savefig('./data/output/figs/06_omega_parameter.png',
            bbox_inches='tight',pad_inches = 0.1, dpi = 125)
plt.close()


###

import xarray as xr
import glob
import geopandas as gpd
import rioxarray

eps = gpd.read_file("./data/raw/EPSs/runoff/C_aporte.shp")

fig, ax = plt.subplots()
eps.boundary.plot(ax = ax)
eps.iloc[[10, 33]].plot(ax = ax)

time_Step = np.arange(1982, 2017).tolist()
time_Step = [str(i) for i in time_Step]
qmax_ts = []
qmin_ts = []
qmean_ts = []

for times in time_Step:
    qmean = xr.open_dataset("./data/processed/runoff/" + "Q_" + times + ".nc")
    qmean_ts_time = qmean.isel(realization=1).runoff
    qmin_ts_time = qmean.isel(realization=2).runoff
    qmax_ts_time = qmean.isel(realization=0).runoff
    qmean_ts_time = qmean_ts_time.rio.set_crs("epsg:4326")
    qmin_ts_time = qmin_ts_time.rio.set_crs("epsg:4326")
    qmax_ts_time = qmax_ts_time.rio.set_crs("epsg:4326")

    subx = eps.iloc[10: 10 + 1]
    qmean_ts_time = qmean_ts_time.rio.clip(subx.geometry).mean().values
    qmin_ts_time = qmin_ts_time.rio.clip(subx.geometry).mean().values
    qmax_ts_time = qmax_ts_time.rio.clip(subx.geometry).mean().values

    qmax_ts.append(float(qmax_ts_time))
    qmin_ts.append(float(qmin_ts_time))
    qmean_ts.append(float(qmean_ts_time))

q_eps_10 = pd.concat([pd.DataFrame(qmin_ts), pd.DataFrame(qmean_ts), pd.DataFrame(qmax_ts)], axis=1)
q_eps_10.columns = ["qmin", "qmean", "qmax"]

qmax_ts = []
qmin_ts = []
qmean_ts = []

for times in time_Step:
    qmean = xr.open_dataset("./data/processed/runoff/" + "Q_" + times + ".nc")
    qmean_ts_time = qmean.isel(realization=1).runoff
    qmin_ts_time = qmean.isel(realization=2).runoff
    qmax_ts_time = qmean.isel(realization=0).runoff
    qmean_ts_time = qmean_ts_time.rio.set_crs("epsg:4326")
    qmin_ts_time = qmin_ts_time.rio.set_crs("epsg:4326")
    qmax_ts_time = qmax_ts_time.rio.set_crs("epsg:4326")

    subx = eps.iloc[33: 33 + 1]
    qmean_ts_time = qmean_ts_time.rio.clip(subx.geometry).mean().values
    qmin_ts_time = qmin_ts_time.rio.clip(subx.geometry).mean().values
    qmax_ts_time = qmax_ts_time.rio.clip(subx.geometry).mean().values

    qmax_ts.append(float(qmax_ts_time))
    qmin_ts.append(float(qmin_ts_time))
    qmean_ts.append(float(qmean_ts_time))

q_eps_55 = pd.concat([pd.DataFrame(qmin_ts), pd.DataFrame(qmean_ts), pd.DataFrame(qmax_ts)], axis=1)
q_eps_55.columns = ["qmin", "qmean", "qmax"]

fig, (ax, ax1) = plt.subplots(2, 1, figsize = (6, 5), constrained_layout=True, dpi = 120, sharex=True)

ax.plot(np.arange(1982, 2017), q_eps_10["qmean"].tolist(), c="black")
ax.fill_between(np.arange(1982, 2017), (q_eps_10["qmin"].tolist()), (q_eps_10["qmax"].tolist()), color='gray', alpha=.1)
ax.set_title(eps.iloc[10: 10 + 1].nomcuenca.tolist()[0])
ax1.plot(np.arange(1982, 2017), q_eps_55["qmean"].tolist(), c="black")
ax1.fill_between(np.arange(1982, 2017), (q_eps_55["qmin"].tolist()), (q_eps_55["qmax"].tolist()), color='gray', alpha=.1)
ax1.set_title(eps.iloc[33: 33 + 1].nomcuenca.tolist()[0])
ax.set_ylabel("Escurrimiento (mm/año)")
ax1.set_ylabel("Escurrimiento (mm/año)")
ax.grid(True, linestyle='--', color = "black", alpha = 0.1)
ax1.grid(True, linestyle='--', color = "black", alpha = 0.1)

plt.savefig('./data/output/figs/06_example_runoff.png',
            bbox_inches='tight',pad_inches = 0.1, dpi = 125)
plt.close()