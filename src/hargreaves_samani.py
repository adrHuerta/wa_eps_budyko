def hargreaves_samani(tx_i,
                      tn_i,
                      date_i,
                      lat_i):

    delta = np.sin((2 * np.pi * date_i / 365) - 1.405) * 0.4093
    d_r = 1 + 0.033 * np.cos(2 * np.pi * date_i / 365)
    W_s = np.arccos(-np.tan(np.radians(lat_i)) * np.tan(delta))
    Re = 15.392 * d_r * (
                W_s * np.sin(np.radians(lat_i)) * np.sin(delta) +
                np.cos(np.radians(lat_i)) * np.cos(delta) * np.sin(W_s)
    )

    return (np.sqrt((tx_i - tn_i)) * ((tx_i + tn_i) / 2 + 17.8) * Re * 0.0023)
