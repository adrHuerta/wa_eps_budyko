import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})

hydro_time = pd.date_range("1982-01-01", "2016-12-31", freq="M")

# obs data
qobs_xyz = pd.read_excel("./data/raw/Caudal/Qobs_monthly_peru.xlsx", sheet_name="Metadata")
qobs_xyz = qobs_xyz[~qobs_xyz["Abrev"].isin(["LNA", "PCQ"])]
qobs_xyz = qobs_xyz.sort_values(by="Abrev")
qobs_xyz.reset_index(inplace=True)
qobs_xyz = qobs_xyz.drop(["index", 'GR2M_ID', 'Remove'], axis = 1)

# obs time serie data
qobs_ts = pd.read_excel("./data/raw/Caudal/Qobs_monthly_peru.xlsx", sheet_name="Values", header=0, skiprows=[0,1])
qobs_dates = qobs_ts["Abrev."].iloc[2:].values
qobs_ts = qobs_ts[qobs_xyz["Abrev"].values].iloc[2:]
qobs_ts = qobs_ts.set_index(qobs_dates)
qobs_ts = qobs_ts.loc["1981-09-01":"2016-08-31"]
qobs_ts = qobs_ts.set_index(hydro_time)
# qobs_ts = qobs_ts.resample("1Y").apply(lambda x: np.nanmean(x) if np.sum(~np.isnan(x)) > 10 else np.nan)
qobs_ts = qobs_ts.resample("1Y").apply(lambda x: np.mean(x))

fig, (ax, ax1, ax2) = plt.subplots(3, 1, dpi=110, figsize=(5, 20))

all_data = qobs_ts.apply(lambda x: np.sum(~np.isnan(x)), axis=1).values
all_data_30 = qobs_ts.loc[:, (qobs_ts.apply(lambda x: np.sum(~np.isnan(x)), axis=0) > 30)].apply(lambda x: np.sum(~np.isnan(x)), axis=1)
all_data_20 = qobs_ts.loc[:, (qobs_ts.apply(lambda x: np.sum(~np.isnan(x)), axis=0) > 20)].apply(lambda x: np.sum(~np.isnan(x)), axis=1)
all_data_15 = qobs_ts.loc[:, (qobs_ts.apply(lambda x: np.sum(~np.isnan(x)), axis=0) > 15)].apply(lambda x: np.sum(~np.isnan(x)), axis=1)
all_data_10 = qobs_ts.loc[:, (qobs_ts.apply(lambda x: np.sum(~np.isnan(x)), axis=0) > 10)].apply(lambda x: np.sum(~np.isnan(x)), axis=1)

ax.plot(qobs_ts.index.strftime("%Y").astype(int), all_data, label='Sin Filtro', marker=1)
ax.plot(qobs_ts.index.strftime("%Y").astype(int), all_data_30, label='30', marker=2)
ax.plot(qobs_ts.index.strftime("%Y").astype(int), all_data_20, label='20', marker=3)
ax.plot(qobs_ts.index.strftime("%Y").astype(int), all_data_15, label='15', marker=4)
ax.plot(qobs_ts.index.strftime("%Y").astype(int), all_data_10, label='10', marker=5)
ax.set_ylabel("Cantidad de datos")
ax.legend(loc='upper left')

all_data_15 = qobs_ts.loc[:, (qobs_ts.apply(lambda x: np.sum(~np.isnan(x)), axis=0) > 15)].loc["2000-01-01":"2016-12-31"]

for line_i in all_data_15.columns:
    ax1.plot(all_data_15.index.strftime("%Y").astype(int),
             all_data_15[line_i].values,
             label=line_i)
#ax1.legend(loc='upper left', prop={'size': 6},  ncol=12)
ax1.set_ylabel("Caudal (m³/s)")
ax1.set_ylim(500, 45000)

for line_i in all_data_15.columns:
    ax2.plot(all_data_15.index.strftime("%Y").astype(int),
             all_data_15[line_i].values,
             label=line_i)
ax2.legend(loc='upper center', prop={'size': 4.5},  ncol=7)
ax2.set_ylabel("Caudal (m³/s)")
ax2.set_ylim(0, 300)

plt.savefig('./data/output/figs/03_runoff_availability.png',
            bbox_inches='tight',pad_inches = 0, dpi = 125)
plt.close()


qobs_xyz[qobs_xyz["Abrev"].isin(all_data_15.columns)]