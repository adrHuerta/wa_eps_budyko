import pandas as pd
import numpy as np
import geopandas as gpd
import pickle

hydro_time = pd.date_range("1982-01-01", "2016-12-31", freq="M")

# obs data
qobs_xyz = gpd.read_file("./data/raw/Caudal/PEQ_1981-2020_subcuencas_GR2M_Peru_SHP/Subbasins_GR2M_Peru.shp")
qobs_xyz["GR2M_ID"] = qobs_xyz["GR2M_ID"].apply(lambda x: "GR2M_ID" + "_" + str(x))

# caudal
qobs_ts_q = pd.read_excel("/home/adrian/Documents/Repos/wa_eps_budyko/data/raw/Caudal/PEQ_1981-2020_subcuencas_GR2M_Peru.xlsx",
                          sheet_name="Q_mm")
qobs_dates_q = qobs_ts_q["Fecha"]
qobs_ts_q = qobs_ts_q.drop(["Fecha"], axis=1)
qobs_ts_q = qobs_ts_q.set_index(qobs_dates_q)
qobs_ts_q = qobs_ts_q.loc["1981-09-01":"2016-08-31"]
qobs_ts_q = qobs_ts_q.set_index(hydro_time)
qobs_ts_q = qobs_ts_q.resample("1Y").apply(lambda x: np.sum(x))

"""
# esta en mm
qobs_ts_q_mm = qobs_dates_q.copy()

for cuenca in qobs_ts.columns.values:
    #qobs_ts_mm[cuenca] = qobs_ts[cuenca]* 36*24*12*3/ list(shps_qobs[shps_qobs["Outlet"] == cuenca].to_crs({'init': 'epsg:32717'}).area / 10**6)
    qobs_ts_mm[cuenca] = qobs_ts[cuenca]* 86400*1000*30.41*12 / list(qobs_xyz[qobs_xyz["GR2M_ID"] == cuenca].to_crs({'init': 'epsg:32717'}).area)

"""

# precipitation
qobs_ts_p = pd.read_excel("/home/adrian/Documents/Repos/wa_eps_budyko/data/raw/Caudal/PEQ_1981-2020_subcuencas_GR2M_Peru.xlsx",
                          sheet_name="P_mm")
qobs_dates_p = qobs_ts_p["Fecha"]
qobs_ts_p = qobs_ts_p.drop(["Fecha"], axis=1)
qobs_ts_p = qobs_ts_p.set_index(qobs_dates_p)
qobs_ts_p = qobs_ts_p.loc["1981-09-01":"2016-08-31"]
qobs_ts_p = qobs_ts_p.set_index(hydro_time)
qobs_ts_p = qobs_ts_p.resample("1Y").apply(lambda x: np.sum(x))

# evp
qobs_ts_e = pd.read_excel("/home/adrian/Documents/Repos/wa_eps_budyko/data/raw/Caudal/PEQ_1981-2020_subcuencas_GR2M_Peru.xlsx",
                          sheet_name="E_mm")
qobs_dates_e = qobs_ts_e["Fecha"]
qobs_ts_e = qobs_ts_e.drop(["Fecha"], axis=1)
qobs_ts_e = qobs_ts_e.set_index(qobs_dates_e)
qobs_ts_e = qobs_ts_e.loc["1981-09-01":"2016-08-31"]
qobs_ts_e = qobs_ts_e.set_index(hydro_time)
qobs_ts_e = qobs_ts_e.resample("1Y").apply(lambda x: np.sum(x))

qobs = {}
keys = qobs_ts_q.index.strftime("%Y").to_list()
for i in keys:

    shps_qobs_key = qobs_xyz.copy()

#    if i == "clim":
#        shps_qobs_key["Q"] = qobs_ts_mm.mean(axis=0).values
#    else:
#

    shps_qobs_key["Q"] = qobs_ts_q[qobs_ts_q.index.strftime("%Y").isin([i])].values[0]
    shps_qobs_key["P"] = qobs_ts_p[qobs_ts_p.index.strftime("%Y").isin([i])].values[0]
    shps_qobs_key["E"] = qobs_ts_e[qobs_ts_e.index.strftime("%Y").isin([i])].values[0]

    qobs[i] = shps_qobs_key

pickle.dump(qobs, open("./data/processed/qobs.pkl","wb"))


"""
####

# # not used
# # Los Naranjos /LNA y Atlantic-Puente Corral Quemado -PCQ

def r2rs(x):
    if x == "Atlantic":
        return "Atlántico"
    elif x == "Pacific":
        return "Pacífico"
    else:
        return "Titicaca"

##
hydro_time = pd.date_range("1982-01-01", "2016-12-31", freq="M")

# obs data
qobs_xyz = pd.read_excel("./data/raw/Caudal/Qobs_monthly_peru.xlsx", sheet_name="Metadata")
qobs_xyz = qobs_xyz[~qobs_xyz["Abrev"].isin(["LNA", "PCQ"])]
qobs_xyz = qobs_xyz.sort_values(by="Abrev")
qobs_xyz.reset_index(inplace=True)
qobs_xyz = qobs_xyz.drop(["index", 'GR2M_ID', 'Remove'], axis = 1)
qobs_xyz["Region"] = qobs_xyz["Region"].apply(lambda x: r2rs(x))

# obs time serie data
qobs_ts = pd.read_excel("./data/raw/Caudal/Qobs_monthly_peru.xlsx", sheet_name="Values", header=0, skiprows=[0,1])
qobs_dates = qobs_ts["Abrev."].iloc[2:].values
qobs_ts = qobs_ts[qobs_xyz["Abrev"].values].iloc[2:]
qobs_ts = qobs_ts.set_index(qobs_dates)
qobs_ts = qobs_ts.loc["1981-09-01":"2016-08-31"]
qobs_ts = qobs_ts.set_index(hydro_time)
qobs_ts = qobs_ts.resample("1Y").apply(lambda x: np.mean(x))

# filtering to 2000-2016 and station with more than 15 years of data
qobs_ts = qobs_ts.loc[:, (qobs_ts.apply(lambda x: np.sum(~np.isnan(x)), axis=0) > 15)].loc["2000-01-01":"2016-12-31"]
qobs_ts_mm = qobs_ts.copy()

# shapefiles
shps_qobs = ["./data/raw/Caudal/Areas_drenaje_Qm/Area_" + str(i) + ".shp" for i in qobs_ts.columns.to_list()]
shps_qobs = [gpd.read_file(i) for i in shps_qobs]
shps_qobs = gpd.GeoDataFrame(pd.concat(shps_qobs))
shps_qobs.reset_index(inplace=True)
shps_qobs = shps_qobs.drop(["index","Area","Region","GR2M_ID"], axis=1)
shps_qobs["Vertiente"] = shps_qobs["Vertiente"].apply(lambda x: r2rs(x))

for cuenca in qobs_ts.columns.values:
    #qobs_ts_mm[cuenca] = qobs_ts[cuenca]* 36*24*12*3/ list(shps_qobs[shps_qobs["Outlet"] == cuenca].to_crs({'init': 'epsg:32717'}).area / 10**6)
    qobs_ts_mm[cuenca] = qobs_ts[cuenca]* 86400*1000*30.41*12 / list(shps_qobs[shps_qobs["Outlet"] == cuenca].to_crs({'init': 'epsg:32717'}).area)

qobs = {}
keys = ["clim"] + qobs_ts_mm.index.strftime("%Y").to_list()
for i in keys:

    shps_qobs_key = shps_qobs.copy()

    if i == "clim":
        shps_qobs_key["Q"] = qobs_ts_mm.mean(axis=0).values
    else:
        shps_qobs_key["Q"] = qobs_ts_mm[qobs_ts_mm.index.strftime("%Y").isin([i])].values[0]

    qobs[i] = shps_qobs_key

qobs["clim"]["Q"] == qobs["2000"]["Q"]
pickle.dump(qobs, open("./data/processed/qobs.pkl","wb"))
qobs_xyz[qobs_xyz["Abrev"].isin(qobs_ts_mm.columns)].to_csv("./data/processed/qobs_xyz.csv", index=False)
"""