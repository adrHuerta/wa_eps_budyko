def get_q(p,
          pet,
          w):
    Q = p * np.power(1 + np.power((pet + 0.0001)/ (p + 0.0001), w), 1 / w) - pet
    return Q


def get_q2(p,
           pet,
           w):
    Q = p * np.power(1 + np.power((pet + 0.0001) / (p + 0.0001), w), 1 / w) - pet
    if Q < 0:
        Q = 0
    return Q


def calib_Budyko(q,
                 p,
                 pet,
                 omega=np.arange(1.1, 20.01, .01)):
    qcal = [get_q(p=p, pet=pet, w=omega_values) for omega_values in omega]
    qcal_error = [np.sqrt(i - q) for i in qcal]
    best_omega = omega[np.argmax(qcal_error)]

    return best_omega
