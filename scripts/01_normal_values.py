import xarray as xr
import numpy as np
from pandas import date_range as pd_date_range
from cdo import *
cdo = Cdo()

# PET function
exec(open("./src/ai_fao.py").read())

# hydrological time
hydro_time = pd_date_range("1982-01-01", "2016-12-31", freq="D")
hydro_time = hydro_time[~((hydro_time.day == 29) & (hydro_time.month == 2))]
hydro_time2 = pd_date_range("1982-01-01", "2016-12-31", freq="M")

# pet
piscopet = xr.open_dataset(cdo.cat(input="./data/raw/PET/*.nc"))
#piscopet = piscopet.rename({"__xarray_dataarray_variable__":"pet"})
piscopet = piscopet.sel(time=slice("1981-09-01", "2016-08-31"))
piscopet = piscopet.isel(time=~piscopet.time.dt.strftime('%m-%d').isin("02-29"))
piscopet["time"] = hydro_time

piscopet_anual = piscopet.resample(time="1Y").sum()
piscopet_anual = piscopet_anual.reindex(longitude=np.arange(piscopet.longitude.values[1], piscopet.longitude.values[-1], 0.008),
                                    latitude=np.arange(piscopet.latitude.values[1], piscopet.latitude.values[-1], -0.008),
                                    method="nearest")
# precp
piscop = xr.open_dataset("./data/raw/PISCO/PISCOpd.nc")
piscop = piscop.rename({"z":"time"})
piscop = piscop.sel(time=slice("1981-09-01", "2016-08-31"))
piscop = piscop.isel(time=~piscop.time.dt.strftime('%m-%d').isin("02-29"))
piscop["time"] = hydro_time

piscop_anual = piscop.resample(time="1Y").sum()
piscop_anual = piscop_anual.reindex(longitude=np.arange(piscopet.longitude.values[1], piscopet.longitude.values[-1], 0.008),
                                    latitude=np.arange(piscopet.latitude.values[1], piscopet.latitude.values[-1], -0.008),
                                    method="nearest")


pisco_data = xr.Dataset({'p': piscop_anual.p, 'pet': piscopet_anual.pet})
#pisco_data["ai"] = pisco_data.groupby('time').apply(ai_fao)

# saving data
pisco_data.to_netcdf("./data/processed/pisco_data.nc")