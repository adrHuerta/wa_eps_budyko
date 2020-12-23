import xarray as xr
import pandas as pd
import pickle
import rioxarray

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.1, rc={"lines.linewidth": 2})

exec(open("./src/metrics.py").read())

mean_spatial_runoff = xr.open_dataset("./data/processed/mean_spatial_runoff.nc").runoff
spatial_runoff_2000_2016 = xr.open_dataset("./data/processed/2000_2016_spatial_runoff.nc").runoff
shp_obs = pickle.load(open("./data/processed/qobs.pkl","rb"))
budyko = pickle.load(open("./data/processed/calibrated_omega_by_time.pkl","rb"))
budyko_cv = pickle.load(open("./data/processed/budyko_Qest_CV.pkl","rb"))

# calibrated omega

df_calibrated_omega = []
for i in range(len(budyko)):
    df_data = pd.DataFrame(budyko[i])
    df_data.columns = ["Omega", "NSE"]
    df_data["Vertiente"] = ["Atlántico", "Pacífico", "Titicaca"]
    df_data["Año"] = i
    df_calibrated_omega.append(df_data[["Vertiente", "Año", "Omega", "NSE"]])

pd.concat(df_calibrated_omega, axis=0).to_csv("./data/output/figs/tab_calibrated_omega.csv")

# obs-basin vs gridded runoff
for times in shp_obs.keys():

    Qest = []

    if times == "clim":
        spatial_runoff = mean_spatial_runoff
    else:
        spatial_runoff = spatial_runoff_2000_2016[spatial_runoff_2000_2016.time.dt.strftime("%Y") == times]

    spatial_runoff = spatial_runoff.rio.set_crs("epsg:4326")

    for i in range(len(shp_obs[times].Outlet)):
        subx = shp_obs[times].iloc[i: i + 1]
        Qcalc = spatial_runoff.rio.clip(subx.geometry).mean().values.tolist()
        Qest.append(Qcalc)

    shp_obs[times]["Qest"] = Qest


fig, (ax1, ax) = plt.subplots(1, 2, sharex=True, sharey=True, dpi=150, figsize=(10, 4))
# cross-validation (mean runoff)
sns.scatterplot(x="Q", y="Qest_cv", data=pd.DataFrame(budyko_cv["clim"]), hue="Vertiente", s=30, ax=ax1)
ax1.set_xlabel("Caudal promedio observado (mm)")
ax1.set_ylabel("Caudal promedio simulado (mm)")
ax1.set_ylim(0, 3500)
ax1.set_xlim(0, 3500)
ax1.text(2200, 850, "NSE: " + str(nse_m(obs=budyko_cv["clim"].Q, sim=budyko_cv["clim"].Qest_cv)), fontsize=10)
ax1.text(2200, 700, "WBE: " + str(wbe_m(obs=budyko_cv["clim"].Q, sim=budyko_cv["clim"].Qest_cv)), fontsize=10)
ax1.text(2200, 550, "RMSE: " + str(rmse_m(obs=budyko_cv["clim"].Q, sim=budyko_cv["clim"].Qest_cv)), fontsize=10)

# comparison (mean runoff)
sns.scatterplot(x="Q", y="Qest", data=pd.DataFrame(shp_obs["clim"]), hue="Vertiente", s=30, ax=ax)
ax.set_xlabel("Caudal promedio observado (mm)")
ax.set_ylabel("Caudal promedio simulado (mm)")
ax.set_ylim(0, 3500)
ax.set_xlim(0, 3500)
ax.get_legend().remove()
ax.text(2200, 850, "NSE: " + str(nse_m(obs=shp_obs["clim"].Q, sim=shp_obs["clim"].Qest)), fontsize=10)
ax.text(2200, 700, "WBE: " + str(wbe_m(obs=shp_obs["clim"].Q, sim=shp_obs["clim"].Qest)), fontsize=10)
ax.text(2200, 550, "RMSE: " + str(rmse_m(obs=shp_obs["clim"].Q, sim=shp_obs["clim"].Qest)), fontsize=10)

plt.savefig('./data/output/figs/05_CV_comparison.png',
            bbox_inches='tight',pad_inches = 0, dpi = 150)
plt.close()

# metrics from comparison (time_serie data)
metrics_s = [(nse_m(obs=shp_obs[times].Q, sim=shp_obs[times].Qest),
              wbe_m(obs=shp_obs[times].Q, sim=shp_obs[times].Qest),
              rmse_m(obs=shp_obs[times].Q, sim=shp_obs[times].Qest)) for times in list(shp_obs.keys())[1:]]

df_metrics_s = []
for i in range(len(metrics_s)):
    df_data = pd.DataFrame(metrics_s[i]).transpose()
    df_data.columns = ["NSE", "WBE", "RMSE"]
    df_data["Año"] = i
    df_metrics_s.append(df_data[["Año", "NSE", "WBE", "RMSE"]])

pd.concat(df_metrics_s, axis=0).to_csv("./data/output/figs/tab_metrics_comparison.csv")


fig, axes = plt.subplots(ncols=6, nrows=6, sharex=True)
for ax, stations in zip(axes.flat, list(range(shp_obs["clim"].shape[0]))):
    ax.plot([shp_obs[time]["Q"].iloc[stations] for time in list(shp_obs.keys())[1:]])
    ax.plot([shp_obs[time]["Qest"].iloc[stations] for time in list(shp_obs.keys())[1:]])
    ax.set_title(shp_obs["clim"]["Outlet"].iloc[stations] + "_" + shp_obs["clim"]["Vertiente"].iloc[stations])
