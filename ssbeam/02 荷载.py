import numpy as np
import pandas as pd
from sectionproperties.analysis import Section

from src.Nu2000Sect import comp_sections, un2k, C65
from src.mechanics import calculate


def get_env(flist, dist, span, m_loc, s_loc):
    moment = []
    shear = []
    dd = [0, ]
    for dx in dist:
        dd.append(dd[-1] + dx)
    x0 = 0
    x1 = sum(span) - sum(dist)
    for xx in np.linspace(x0, x1, int((x1 - x0) / 1)):
        if abs(xx - 20) <= 3:
            br = True
        m = np.zeros(len(m_loc))
        s = np.zeros(len(s_loc))
        for ii, f in enumerate(flist):
            res = calculate(span, cForce=[xx + dd[ii]], moment_loc=m_loc, shear_loc=s_loc, cForce_ft=[f, ])
            m += np.array(res['m'])
            s += np.array(res['s'])
        moment.append(m)
        shear.append(s)
    moment = np.mat(moment)
    shear = np.mat(shear)
    return moment.min(0), moment.max(0), shear.min(0), shear.max(0)


if __name__ == '__main__':
    # A	I_g	y_{bg} 	y_{tg}	y_t
    G1 = [0.722, 0.371, 0.930, 1.070, 1.070]
    C1 = [1.511, 0.934, 1.546, 0.454, 0.779]
    G2 = [2.036, 0.688, 1.008, 0.992, 0.992]
    C2 = [2.826, 1.411, 1.307, 0.693, 1.018]

    print("Beam self-weight = %.3f/%.3f (middle/end section) kN/m" % (G1[0] * 26, G2[0] * 26))
    print("Slab weight = %.3f kN/m" % (1.80 * 26 * 0.5))
    print("Diaphragm weight = %.3f kN/per diaphragm" % (1.040 * 0.25 * 3.1 * 0.5 * 26))
    xloc40 = [0, 0.8, 1.6, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    calculate([40, ], cForce=[20 - 4.3, 20, 20 + 4.3], moment_loc=[20, ], cForce_ft=[35e3, 145e3, 145e3])

    m1 = calculate([40, ], dForce=[1.6, 40 - 1.6], moment_loc=xloc40, shear_loc=xloc40)
    m2 = calculate([40, ], dForce=[0, 1.6], moment_loc=xloc40, shear_loc=xloc40)
    m3 = calculate([40, ], dForce=[40 - 1.6, 40], moment_loc=xloc40, shear_loc=xloc40)
    mall = calculate([40, ], dForce=[0, 40], moment_loc=xloc40, shear_loc=xloc40)
    DCm = (np.array(m1['m']) * 18.772 +
           np.array(m2['m']) * 52.936 +
           np.array(m3['m']) * 52.936)
    DCv = (np.array(m1['s']) * 18.772 +
           np.array(m2['s']) * 52.936 +
           np.array(m3['s']) * 52.936)
    DWm = np.array(mall['m']) * 17.3
    DWv = np.array(mall['s']) * 17.3
    Lane_m = np.array(mall['m']) * 9.3 * 0.81
    Lane_v = np.array(mall['s']) * 9.3 * 0.81
    Truck_m = get_env(flist=[35 * 0.81, 145 * 0.81, 145 * 0.81, ], span=[40, ], dist=[4.3, 4.3], m_loc=xloc40, s_loc=xloc40)[0]
    Td_m = get_env(flist=[108 * 0.81, 108 * 0.81, ], span=[40, ], dist=[1.2, ], m_loc=xloc40, s_loc=xloc40)[0]
    Truck_m = np.array(Truck_m)[0]
    Td_m = np.array(Td_m)[0]
    for i, x in enumerate(xloc40):
        print("%.1f\t%.1f\t%.1f\t%.1f\t%.1f\t%.1f" % (x, DCm[i], DWm[i], Lane_m[i], Truck_m[i], Td_m[i]))
    for i, x in enumerate(xloc40):
        print("%.1f\t%.1f\t%.1f" % (x, DCv[i], DWv[i],))
    xloc33 = [0, 0.8, 1.6, 2, 4, 6, 8, 10, 12, 14, 16.5]
    m1 = calculate([33, ], dForce=[1.6, 33 - 1.6], moment_loc=xloc33, shear_loc=xloc33)
    m2 = calculate([33, ], dForce=[0, 1.6], moment_loc=xloc33, shear_loc=xloc33)
    m3 = calculate([33, ], dForce=[33 - 1.6, 33], moment_loc=xloc33, shear_loc=xloc33)
    mall = calculate([33, ], dForce=[0, 33], moment_loc=xloc33, shear_loc=xloc33)
    DCm = (np.array(m1['m']) * 18.772 +
           np.array(m2['m']) * 52.936 +
           np.array(m3['m']) * 52.936)
    DCv = (np.array(m1['s']) * 18.772 +
           np.array(m2['s']) * 52.936 +
           np.array(m3['s']) * 52.936)
    DWm = np.array(mall['m']) * 17.3
    DWv = np.array(mall['s']) * 17.3
    for i, x in enumerate(xloc33):
        print("%.1f\t%.1f\t%.1f" % (x, DCm[i], DWm[i]))
    for i, x in enumerate(xloc33):
        print("%.1f\t%.1f\t%.1f" % (x, DCv[i], DWv[i]))
