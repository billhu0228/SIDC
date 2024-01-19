import pint
import numpy as np
from pint import UnitRegistry

ureg: UnitRegistry = pint.UnitRegistry()
Q_ = ureg.Quantity


def Get_Si(L, W, hri):
    return L * W / (2 * hri * (L + W))


def Get_eps(sigma, G, S):
    return sigma / (4.8 * G * S ** 2)


def A(e):
    return (2 * e ** 2 - 2 * 100 * e) / (1 - e / 100)


if __name__ == "__main__":

    """
    Method B AASHTO 14.7.5 
    """
    # 1 基础参数
    L = Q_(420, ureg.mm).to(ureg.inch)
    W = Q_(470, ureg.mm).to(ureg.inch)
    hri = Q_(12, ureg.mm).to(ureg.inch)
    S = L * W / (2 * hri * (L + W))  # 形状系数
    print("最小PTFE厚度  Th=%.0f mm" % Q_(0.1875, ureg.inch).to(ureg.mm).m)
    print("形状系数  Si=%.1f" % S.m)
    G = Q_(0.9, ureg.MPa).to(ureg.ksi)  # 剪切模量

    theta_dc = Q_(1.45 * 1e-3, 1 / ureg.rad)
    theta_ll = Q_(1.25 * 1e-3, 1 / ureg.rad)
    theta_allowance = Q_(5.0 * 1e-3, 1 / ureg.rad)

    DCDW = Q_(1140, ureg.kN).to(ureg.kip)  # 边支座恒载
    # DCDW = Q_(3140, ureg.kN).to(ureg.kip)  # 边支座恒载
    LL_min = Q_(165, ureg.kN).to(ureg.kip)  # 边支座活载
    LL_max = Q_(490, ureg.kN).to(ureg.kip)  # 边支座活载
    FrcCoff = 0.03
    K_l = 2.0 * (ureg.kN / ureg.mm)
    deltaS = FrcCoff * (DCDW + LL_max) / K_l
    # --------------------------------
    n = int(2 * deltaS / hri) + 1 + 2
    hrt = hri * n + (5 * ureg.mm)
    K_l_check = G * W * L / hrt
    print(K_l.to(ureg.kN / ureg.mm), K_l_check.to(ureg.kN / ureg.mm))
    print("剪切变形 Ds= %.1f mm , 橡胶层数 n=%i, 橡胶层总厚度 hrt=%.1f mm" % (deltaS.to(ureg.mm).m, n, hrt.to(ureg.mm).m))
    print("橡胶支座总高 = %.1f mm" % (hrt.to(ureg.mm).m + 3 * (n + 1)))

    sigma_p = DCDW / (L * W)
    sigma_a = (DCDW + LL_max) / (L * W)
    print("恒载平均应力 = %.1f ksi" % sigma_p.to(ureg.ksi).m)
    print("总平均应力 = %.1f ksi" % sigma_a.to(ureg.ksi).m)

    # 14.7.5.3.3 压转剪组合
    gamma_ast = 1.4 * DCDW / (L * W) / (G * S)
    gamma_rst = 0.5 * (L / hri) ** 2 * ((theta_dc + theta_allowance) / n)
    gamma_sst = deltaS / hrt

    gamma_acy = 1.4 * LL_max / (L * W) / (G * S)
    gamma_rcy = 0.5 * (L / hri) ** 2 * ((theta_ll + theta_allowance) / n)
    gamma_scy = deltaS / hrt

    gst = 0
    gcy = 0
    for g in [gamma_ast, gamma_rst, gamma_sst, ]:
        print("%.1f" % g.to(ureg.dimensionless))
        gst += g.to(ureg.dimensionless)
    for g in [gamma_acy, gamma_rcy, gamma_scy, ]:
        print("%.1f" % g.to(ureg.dimensionless))
        gcy += g.to(ureg.dimensionless)
    g_all = gst + 1.75 * gcy
    if g_all < 5.0:
        print("剪应变 ： %.1f < 5.0 , Pass" % g_all.m)
    else:
        print("剪应变 ： %.1f > 5.0 , Fail !!" % g_all.m)
    # 稳定性
    A = (1.92 * hrt / L) / np.sqrt(1 + 2 * L / W)
    B = 2.67 / (S + 2.0) / (1 + L / (4.0 * W))
    # print(A, B)
    if 2 * A <= B:
        print("Stability Check OK!")
    else:
        print("Stability Check Fail!")
        sigma_max = G * S / (2 * A - B)
        if sigma_a < sigma_max:
            print("稳定性应力： %.1f <  %.1f,Stability Check Pass by check sigma!" % (sigma_a.to(ureg.MPa).m, sigma_max.to(ureg.MPa).m))
        else:
            print("Stability Check Fail by check sigma!")
