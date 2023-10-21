import numpy as np
import pandas as pd
import pint
import scipy.interpolate
from scipy.interpolate import interp1d
from src import Superstructure
from src.sections import DXFSection
from pint import UnitRegistry

ureg: UnitRegistry = pint.UnitRegistry()
Q_ = ureg.Quantity


def area(d):
    return np.pi * d ** 2 * 0.25


if __name__ == "__main__":
    S1 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, 300, 3100, 0.1)
    ft = 2.5
    fb = -30.7
    th = ft / (ft - fb) * 2000
    print("受拉区高度=%.4f mm" % th)
    hs = np.linspace(2000 - th, 2000, 2000)
    fs = np.linspace(0, ft, 2000)
    dh = hs[2] - hs[1]
    ys = hs + 0.5 * dh
    ys = ys[0:-1]
    dA = np.array([S1.get_w(z) * dh for z in ys])
    get_fs = interp1d(hs, fs)
    dfs = np.array([get_fs(z) for z in ys])
    T = dfs.dot(dA)
    print("受拉区面积=%.1f mm2" % sum(dA))
    print("受拉区拉力%.1f kN" % (T * 1.e-3))
    As = area(10) * 6 + area(12) * 4
    As2 = area(12) * 3 + 8 * area(10)+area(20) * 6
    fys = (30 * ureg.ksi).to(ureg.MPa).m
    print(fys)
    print("受拉区拉力最大值%.1f kN" % ((As * fys) * 1.e-3))
    print("下部受拉区拉力最大值%.1f kN" % ((As2 * fys) * 1.e-3))


