def slope_trend(x):
  if np.all(np.isnan(x)) == True:
    return np.nan
  else:
    trend, h, p, z, Tau, s, var_s, slope, intercept = mk.trend_free_pre_whitening_modification_test(x)
    return slope

def pvalue_trend(x):
  if np.all(np.isnan(x)) == True:
    return np.nan
  else:
    trend, h, p, z, Tau, s, var_s, slope, intercept = mk.trend_free_pre_whitening_modification_test(x)
    return p
