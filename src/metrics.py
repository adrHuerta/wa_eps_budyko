import numpy as np

def nse_m(obs, sim):
    nse = 1 - (np.sum(np.power(obs-sim, 2))/np.sum(np.power(obs-np.mean(sim), 2)))
    return np.round(nse, 2)

def wbe_m(obs, sim):
    wbe = 100*(np.sum(sim)-np.sum(obs))/np.sum(obs)
    return np.round(wbe, 2)

def rmse_m(obs, sim):
    rmse = np.sqrt(np.sum(np.power(sim - obs, 2))/(len(obs)-1))
    return np.round(rmse, 2)