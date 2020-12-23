import xarray as xr
import numpy as np
import pickle
import random
from joblib import Parallel, delayed

exec(open("./src/calib_Budyko.py").read())

budyko = pickle.load(open("./data/processed/budyko.pkl","rb"))
pisco = xr.open_dataset("./data/processed/pisco_data.nc", chunks={'latitude': 50, 'longitude': 50})
cluster_areas = xr.open_dataset("./data/processed/budyko_groups2.nc", chunks={'latitude': 50, 'longitude': 50}).gridded_groups


for times in budyko.keys():
    budyko_time = budyko[times]

    def best_omega_by_station(station):
        error_Qest = []
        for omega_values in np.arange(1.1, 10.1, .1):
            data_station = budyko_time.loc[budyko_time.GR2M_ID == station]
            Qest = get_q(p=data_station.P_basin, pet=data_station.E_basin, w=omega_values)
            error_Qest.append(np.sqrt(np.mean((Qest - (data_station.Q)) ** 2)))

        best_omega = np.arange(1.1, 10.1, .1)[np.argmin(error_Qest)]
        return float(best_omega)

    best_values_by_group = Parallel(n_jobs=6, verbose=50)(
        delayed(best_omega_by_station)(i) for i in budyko_time.GR2M_ID)

    budyko_time["omega_calib"] = best_values_by_group
    random.seed(times, version=2)
    omega1 = random.sample(budyko_time[budyko_time.Region.isin(["A"])].omega_calib.tolist(), 30)
    omega2 = random.sample(budyko_time[budyko_time.Region.isin(["B"])].omega_calib.tolist(), 30)
    omega3 = random.sample(budyko_time[budyko_time.Region.isin(["C"])].omega_calib.tolist(), 30)
    omega4 = random.sample(budyko_time[budyko_time.Region.isin(["D"])].omega_calib.tolist(), 30)
    omega5 = random.sample(budyko_time[budyko_time.Region.isin(["E"])].omega_calib.tolist(), 30)
    omega6 = random.sample(budyko_time[budyko_time.Region.isin(["F"])].omega_calib.tolist(), 30)
    omega7 = random.sample(budyko_time[budyko_time.Region.isin(["G"])].omega_calib.tolist(), 30)
    omega8 = random.sample(budyko_time[budyko_time.Region.isin(["H"])].omega_calib.tolist(), 30)
    omega9 = random.sample(budyko_time[budyko_time.Region.isin(["I"])].omega_calib.tolist(), 30)
    omega10 = random.sample(budyko_time[budyko_time.Region.isin(["J"])].omega_calib.tolist(), 30)
    omega11 = random.sample(budyko_time[budyko_time.Region.isin(["K"])].omega_calib.tolist(), 30)
    omega12 = random.sample(budyko_time[budyko_time.Region.isin(["L"])].omega_calib.tolist(), 30)
    omega13 = random.sample(budyko_time[budyko_time.Region.isin(["M"])].omega_calib.tolist(), 30)
    omega14 = random.sample(budyko_time[budyko_time.Region.isin(["N"])].omega_calib.tolist(), 30)
    calibrated_omega_by_time = [omega1, omega2, omega3, omega4, omega5, omega6, omega7,
                                omega8, omega9, omega10, omega11, omega12, omega13, omega14]

    pickle.dump(calibrated_omega_by_time, open("./data/processed/runoff/omega_" + times + ".pkl","wb"))

    def apply_budyko_all(p, pet, cluster):
        if np.isnan(cluster):
            Q = np.nan
        elif int(cluster) == 1:
            w = omega1
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 2:
            w = omega2
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 3:
            w = omega3
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 4:
            w = omega4
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 5:
            w = omega5
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 6:
            w = omega6
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 7:
            w = omega7
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 8:
            w = omega8
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 9:
            w = omega9
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 10:
            w = omega10
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 11:
            w = omega11
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 12:
            w = omega12
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 13:
            w = omega13
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        else:
            w = omega14
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        res = [np.max(Q), np.mean(Q), np.min(Q)]
        res = [0 if i < 0 else i for i in res]
        return np.round(res, 1)

    PP = pisco.p[pisco.p.time.dt.strftime("%Y") == times]
    PET = pisco.pet[pisco.pet.time.dt.strftime("%Y") == times]

    Qest_gridded_all = xr.apply_ufunc(apply_budyko_all,
                                      PP,
                                      PET,
                                      cluster_areas,
                                      vectorize=True,
                                      output_sizes={"realization": 3},
                                      output_core_dims=[["realization"]],
                                      dask="parallelized",
                                      output_dtypes=['float64'])

    Qest_gridded_all = Qest_gridded_all.to_dataset(name="runoff")
    Qest_gridded_all["realization"] = [0, 1, 2]
    Qest_gridded_all.to_netcdf("./data/processed/runoff/Q_" + times + ".nc")


"""
    def apply_budyko_mean(p, pet, cluster):
        if np.isnan(cluster):
            Q = np.nan
        elif int(cluster) == 1:
            w = omega1
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 2:
            w = omega2
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 3:
            w = omega3
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 4:
            w = omega4
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 5:
            w = omega5
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 6:
            w = omega6
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 7:
            w = omega7
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 8:
            w = omega8
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 9:
            w = omega9
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 10:
            w = omega10
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 11:
            w = omega11
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 12:
            w = omega12
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 13:
            w = omega13
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        else:
            w = omega14
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        res = np.mean(Q)
        if res < 0:
            res = 0

        return np.round(res, 1)
    def apply_budyko_min(p, pet, cluster):
        if np.isnan(cluster):
            Q = np.nan
        elif int(cluster) == 1:
            w = omega1
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 2:
            w = omega2
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 3:
            w = omega3
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 4:
            w = omega4
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 5:
            w = omega5
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 6:
            w = omega6
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 7:
            w = omega7
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 8:
            w = omega8
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 9:
            w = omega9
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 10:
            w = omega10
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 11:
            w = omega11
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 12:
            w = omega12
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 13:
            w = omega13
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        else:
            w = omega14
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        res = np.min(Q)
        if res < 0:
            res = 0

        return np.round(res, 1)
    def apply_budyko_max(p, pet, cluster):
        if np.isnan(cluster):
            Q = np.nan
        elif int(cluster) == 1:
            w = omega1
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 2:
            w = omega2
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 3:
            w = omega3
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 4:
            w = omega4
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        elif int(cluster) == 5:
            w = omega5
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 6:
            w = omega6
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 7:
            w = omega7
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 8:
            w = omega8
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 9:
            w = omega9
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 10:
            w = omega10
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 11:
            w = omega11
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 12:
            w = omega12
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        elif int(cluster) == 13:
            w = omega13
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]
        else:
            w = omega14
            Q = [p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), i), 1 / i) - pet for i in w]

        res = np.max(Q)
        if res < 0:
            res = 0

        return np.round(res, 1)
"""


"""
    Qest_gridded_mean = xr.apply_ufunc(apply_budyko_mean,
                                       PP,
                                       PET,
                                       cluster_areas,
                                       vectorize=True,
                                       dask="parallelized",
                                       output_dtypes=['float64'])

    Qest_gridded_min = xr.apply_ufunc(apply_budyko_min,
                                       PP,
                                       PET,
                                       cluster_areas,
                                       vectorize=True,
                                       dask="parallelized",
                                       output_dtypes=['float64'])

    Qest_gridded_max = xr.apply_ufunc(apply_budyko_max,
                                       PP,
                                       PET,
                                       cluster_areas,
                                       vectorize=True,
                                       dask="parallelized",
                                       output_dtypes=['float64'])

    Qest_gridded_mean.to_dataset(name = "runoff").to_netcdf("./data/processed/runoff/Q_mean_" + times + ".nc")
    Qest_gridded_min.to_dataset(name = "runoff").to_netcdf("./data/processed/runoff/Q_min_" + times + ".nc")
    Qest_gridded_max.to_dataset(name = "runoff").to_netcdf("./data/processed/runoff/Q_max_" + times + ".nc")

"""