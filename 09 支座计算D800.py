import pint
import numpy as np
from pint import UnitRegistry

ureg: UnitRegistry = pint.UnitRegistry()
Q_ = ureg.Quantity


def Get_Si(L, W, hri):
    return L * W / (2 * hri * (L + W))


def Get_eps(sigma, G, S):
    return sigma / (4.8 * G * S ** 2)


if __name__ == "__main__":
    """
    Method B AASHTO 14.7.5 
    """
    # 1 基础参数
    L = Q_(720, ureg.mm).to(ureg.inch)
    W = Q_(720, ureg.mm).to(ureg.inch)
    # D = Q_(800, ureg.mm).to(ureg.inch)
    hri = Q_(8.3, ureg.mm).to(ureg.inch)
    S = L * W / (2 * hri * (L + W))  # 形状系数
    print("形状系数  Si=%.1f" % S.m)
    G = Q_(1.0, ureg.MPa).to(ureg.ksi)  # 剪切模量

    theta_dc = Q_(0.20 * 1e-3, 1 / ureg.rad)
    theta_ll = Q_(0.20 * 1e-3, 1 / ureg.rad)
    theta_allowance = Q_(5.0 * 1e-3, 1 / ureg.rad)

    DCDW = Q_(2320, ureg.kN).to(ureg.kip)  # 中支座恒载
    LL_min = Q_(410, ureg.kN).to(ureg.kip)  # 中支座活载
    LL_max = Q_(800, ureg.kN).to(ureg.kip)  # 中支座活载
    FrcCoff = 0.03
    Dp1 = 0.5 * 7.0 * ureg.mm
    Dp2 = 0.5 * 18.5 * ureg.mm
    CRSH = 0.5 * 31.3 * ureg.mm
    Dt = 1e-5 * 135000 * 0.5 * 12 * ureg.mm
    Ds = 0.65 * Dt + (Dp1 + Dp2 + CRSH)
    Ds_cy = 0.65 * Dt
    Ds_st = (Dp1 + Dp2 + CRSH)
    print("最大剪切变形 = %.0f mm" % Ds.m)
    # --------------------------------
    n = int(2 * Ds / hri) + 1 + 7
    hrt = hri * (n + 2)
    K_l_check = G * W * L / hrt
    print("支座侧向刚度：%.2f kN/mm" % K_l_check.to(ureg.kN / ureg.mm).m)
    print("剪切变形 Ds= %.1f mm , 橡胶层数 n=%i, 橡胶层总厚度 hrt=%.1f mm" % (Ds.to(ureg.mm).m, n, hrt.to(ureg.mm).m))
    print("橡胶支座总高 = %.1f mm" % (hrt.to(ureg.mm).m + 3 * (n + 1)))

    # 14.7.5.3.3 压转剪组合
    gamma_ast = 1.4 * DCDW / (L * W) / (G * S)
    gamma_rst = 0.5 * (L / hri) ** 2 * ((theta_dc + theta_allowance) / n)
    gamma_sst = Ds_st / hrt

    gamma_acy = 1.4 * LL_max / (L * W) / (G * S)
    gamma_rcy = 0.5 * (L / hri) ** 2 * ((theta_ll + theta_allowance) / n)
    gamma_scy = Ds_cy / hrt

    gst = 0
    gcy = 0
    for g in [gamma_ast, gamma_rst, gamma_sst, ]:
        # print("%.1f" % g.to(ureg.dimensionless))
        gst += g.to(ureg.dimensionless)
    for g in [gamma_acy, gamma_rcy, gamma_scy, ]:
        # print("%.1f" % g.to(ureg.dimensionless))
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
        sigma_a = (DCDW + LL_max) / (L * W)
        if sigma_a < sigma_max:
            print("稳定性应力： %.1f <  %.1f,Stability Check Pass by check sigma!" % (sigma_a.to(ureg.MPa).m, sigma_max.to(ureg.MPa).m))
        else:
            print("Stability Check Fail by check sigma!")
