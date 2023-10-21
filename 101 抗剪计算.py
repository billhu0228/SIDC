import numpy as np
import pint

from PyAngle import Angle
import pandas as pd
from scipy.optimize import bisect
from scipy.interpolate import interp1d

from src.sections import DXFSection

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


def angle_to_epsx_func(deg, Mu, dv, Pu, Vu, Es, Ec, Ag, TensileAs, Aps):
    theta = Angle.from_degrees(deg)
    Ep = 195000
    eps_x = (abs(Mu) / dv + 0.5 * Pu + 0.5 * abs(Vu) * (theta.cos() / theta.sin())) / (2 * Es * TensileAs + Ep * Aps)
    if eps_x > 0.001:
        print("# warning: Eps_x=%.6f" % eps_x)
    if eps_x < 0:
        eps_x = (abs(Mu) / dv + 0.5 * Pu + 0.5 * abs(Vu) * (theta.cos() / theta.sin())) / 2 * (Ec * Ag + Es * TensileAs)
    return eps_x - angle_to_epsx_B(deg)


def CheckAASHTO_GS(AxisLoadkN, Shear):
    ad = 25 / (1.1 * 0.9)
    fc = Q_(35, ureg.MPa).to(ureg.ksi)
    Pu = Q_(AxisLoadkN, ureg.kN).to(ureg.kip)
    Ag = Q_(2.66e6, ureg.mm ** 2).to(ureg.inch ** 2)
    # Vc = 0.5 * np.sqrt(fc) / ad * np.sqrt(1 + P / (0.5 * np.sqrt(fc) * Ag)) * 0.8 * Ag
    Av = Q_(8 * 12 * 12 * 0.25 * 3.1415, ureg.mm ** 2).to(ureg.inch ** 2)
    s = Q_(100, ureg.mm).to(ureg.inch)
    b = Q_(2500, ureg.mm).to(ureg.inch)
    h = Q_(1100, ureg.mm).to(ureg.inch)
    rho_w = Av / (b * s)
    nuD = 3.0
    fyh = Q_(500, ureg.MPa).to(ureg.ksi)
    fw = min(2 * rho_w * fyh, Q_(0.35, ureg.ksi))
    alpha = fw.m / 0.15 + 3.67 - nuD
    Part1 = 1 * ureg.ksi + (Pu / (2 * Ag))
    vc_test = 0.032 * alpha * Part1.m * np.sqrt(fc.m)
    vc = min(0.11 * np.sqrt(fc.m), 0.047 * alpha * np.sqrt(fc.m), vc_test)
    vc = Q_(vc, ureg.ksi)
    Vc = (vc * 0.8 * Ag).to(ureg.kN)
    Vs = (Av * fyh * (0.8 * h) / s).to(ureg.kN)
    Vr = 0.9 * (Vc + Vs)
    print("Vc=%.0f,Vs=%.0f,Vr=%.0f, Vr/Vu=%.2f" % (Vc.m, Vs.m, Vr.m, Vr.m / Shear))


def angle_to_epsx_B(deg):
    assert deg >= 23.2
    assert deg <= 36.8
    if deg < 24.7:
        return interp1d([23.2, 24.7], [-0.2, -0.1])(deg)
    elif deg <= 25.5:
        return interp1d([24.7, 25.5], [-0.1, -0.05])(deg)
    elif deg <= 26.2:
        return interp1d([25.5, 26.2], [-0.05, 0])(deg)
    elif deg <= 28.0:
        return interp1d([26.2, 28.0], [0, 0.125])(deg)
    elif deg <= 29.7:
        return interp1d([28.0, 29.7], [0.125, 0.25])(deg)
    elif deg <= 32.7:
        return interp1d([29.7, 32.7], [0.25, 0.5])(deg)
    elif deg <= 35.2:
        return interp1d([32.7, 35.2], [0.5, 0.75])(deg)
    else:
        return interp1d([35.2, 36.8], [0.75, 1.0])(deg)


def angle_to_epsx(deg):
    assert deg >= 20.4
    assert deg <= 36.4
    if deg < 21.0:
        return interp1d([20.4, 21], [-0.1, -0.05])(deg)
    elif deg <= 21.8:
        return interp1d([21, 21.8], [-0.05, 0])(deg)
    elif deg <= 24.3:
        return interp1d([21.8, 24.3], [0, 0.125])(deg)
    elif deg <= 26.6:
        return interp1d([24.3, 26.6], [0.125, 0.25])(deg)
    elif deg <= 30.5:
        return interp1d([26.6, 30.5], [0.25, 0.5])(deg)
    elif deg <= 33.7:
        return interp1d([30.5, 33.7], [0.5, 0.75])(deg)
    else:
        return interp1d([33.7, 36.4], [0.75, 1.0])(deg)


def angle_to_beta(deg):
    assert deg >= 23.2
    assert deg <= 36.8
    if deg < 24.7:
        return interp1d([23.2, 24.7], [2.73, 2.66])(deg)
    elif deg <= 25.5:
        return interp1d([24.7, 25.5], [2.66, 2.65])(deg)
    elif deg <= 26.2:
        return interp1d([25.5, 26.2], [2.65, 2.60])(deg)
    elif deg <= 28.0:
        return interp1d([26.2, 28.0], [2.60, 2.52])(deg)
    elif deg <= 29.7:
        return interp1d([28.0, 29.7], [2.52, 2.44])(deg)
    elif deg <= 32.7:
        return interp1d([29.7, 32.7], [2.44, 2.28])(deg)
    elif deg <= 35.2:
        return interp1d([32.7, 35.2], [2.28, 2.14])(deg)
    else:
        return interp1d([35.2, 36.8], [2.14, 1.96])(deg)


def Area(d):
    return np.pi * d * d * 0.25


def AASHTO_shear_strength_mm(Pu, Mu, Vu, Ag, bv, dv, nAv, Aps):
    phi = 0.9
    fc = 65.0
    Ec65 = 38837
    vu = abs(Vu) / (phi * bv * dv)
    Es = 200000
    TensileAs = Area(12) * 3 + 8 * Area(10)
    vufc = vu / fc
    assert 0.15 < vufc < 0.175
    deg = bisect(angle_to_epsx_func, 23.2, 36.8, args=(Mu, dv, Pu, Vu, Es, Ec65, Ag, TensileAs, Aps))
    theta = Angle.from_degrees(deg)
    beta = angle_to_beta(deg)
    Vc = 0.083 * beta * np.sqrt(fc) * bv * dv
    s = 150
    Av = nAv * 16 * 16 * 0.25 * np.pi
    Vs = (Av * 420 * dv * theta.cos() / theta.sin()) / s
    Vn = Vc + Vs
    if Vn > 0.25 * fc * bv * dv:
        print("# Exceed 0.25fc-bv-dv~")
        Vn = 0.25 * fc * bv * dv
    Vr = 0.9 * Vn
    return [Vr, Vn, theta.to_degrees()]


if __name__ == "__main__":
    # Av_min = 0.083 * np.sqrt(65.0) * 225 * 150 / 420.0
    # print(Av_min, 2 * Area(16))
    S1 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945, 0.1)
    Fz = 1600e3
    Iz = S1.I()
    b = 225
    Sz = 551338.2256 * 1077.4

    tao = 4.0
    print(tao, Fz / (225 * 1500))

    sigma = -0
    p1max = sigma * 0.5 + np.sqrt((sigma * 0.5) ** 2 + tao ** 2)
    print(p1max)

    # S1.addStrand(75, 1860 * 0.75, 8 * 140, )
    # S1.addStrand(125, 1860 * 0.75, 8 * 140, )
    # S1.addStrand(175, 1860 * 0.75, 6 * 140, )
    # S1.addStrand(225, 1860 * 0.75, 2 * 140, )
    # S1.addStrand(1955, 1860 * 0.75, 4 * 140, )
    # print(S1.gc())
    # print(S1.prs().data)

    # r = AASHTO_shear_strength_mm(0, 0, 2400000, 721416.6, 225, 1440, 2, 4 * 12 * 140)
    # print(r)
    # CheckAASHTO_GS(17052, 1439)
    # CheckAASHTO_GS(17946, 1291)
    # CheckAASHTO_GS(17054, 1369)
