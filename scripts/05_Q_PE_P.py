import xarray as xr
import pickle
import rioxarray
from joblib import Parallel, delayed

qobs = pickle.load(open("./data/processed/qobs.pkl","rb"))
pisco = xr.open_dataset("./data/processed/pisco_data.nc")

#ax = pisco.p.isel(time=0).plot()
#qobs["clim"].plot()

for keys in qobs.keys():

    time_qobs = qobs[keys].copy()

    PP = pisco.p[pisco.p.time.dt.strftime("%Y") == keys]
    PET = pisco.pet[pisco.pet.time.dt.strftime("%Y") == keys]
    PP = PP.rio.set_crs("epsg:4326")
    PET = PET.rio.set_crs("epsg:4326")

    def get_data_from_shp(i_basin):
        subx = time_qobs.iloc[i_basin: i_basin + 1]
        PP_basin = PP.rio.clip(subx.geometry).mean().values
        PET_basin = PET.rio.clip(subx.geometry).mean().values
        return float(PP_basin), float(PET_basin)

    num_cores = 4
    PP_and_PET_by_basin = Parallel(n_jobs=num_cores, verbose=50)(delayed(get_data_from_shp)(i) for i in range(time_qobs.shape[0]))
    PP_basin = [PP_and_PET_by_basin[i][0] for i in range(len(PP_and_PET_by_basin))]
    PET_basin = [PP_and_PET_by_basin[i][1] for i in range(len(PP_and_PET_by_basin))]

    time_qobs["P_basin"] = PP_basin
    time_qobs["E_basin"] = PET_basin
    time_qobs["AET_basin"] = PP_basin - time_qobs["Q"]
    time_qobs["Ei_basin"] = time_qobs["AET_basin"] / PP_basin
    time_qobs["Ai_basin"] = time_qobs["E_basin"] / time_qobs["P_basin"]
    pickle.dump(time_qobs, open("./data/processed/budyko/budyko_" + keys + ".pkl", "wb"))
    qobs[keys] = time_qobs

    print(keys)

#qobs["clim"]["Ai"] == qobs["2000"]["Ai"]
#qobs["clim"]["Q"] == qobs["2000"]["Q"]

pickle.dump(qobs, open("./data/processed/budyko.pkl","wb"))
