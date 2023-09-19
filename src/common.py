from srbpy import Align

from src.creep import beta_c

D1 = Align('D1', './Data/EI/D1')
D2 = Align('D2', './Data/EI/D2')
D3 = Align('D3', './Data/EI/D3')
D4 = Align('D4', './Data/EI/D4')
M = Align('M', './Data/EI/M')

import numpy as np

fc = 70.0
fc_slab = 50
fci = 56.0
gc = 2250 + 2.29 * fc
Ec = 0.041 * 1 * gc ** 1.5 * np.sqrt(fc)
Ep = 196e3
Eci = 0.041 * 1 * gc ** 1.5 * np.sqrt(fci)
Ec_slab = 0.041 * 1 * gc ** 1.5 * np.sqrt(fc_slab)
n = Ec_slab / Ec

A = 721016.600
outer = 7483.19
h = 2000.0
I = 3.7064E+11
yb = 929.95
yt = 1070.05
Sb = I / yb
St = I / yt

Ac = 1572516.600
hc = 2325.0
Ic = 9.71258953E+11
ybc = 1566.86
ytg = h - ybc
ytc = hc - ybc
Sbc = Ic / ybc
Stg = Ic / ytg
Stc = Ic / ytc

fpc = 1860 * 0.75

BeamDC = 2500 * 1e-9 * 9.806 * A
DeckDC = 2500 * 1e-9 * 9.806 * 325 * 3100
BarrDC = 2500 * 1e-9 * 9.806 * (2 * 345814.54 + 363302.64) / 7  # 护栏
DW = 2400 * 1e-9 * 9.806 * (120 * 22850) / 7  # 护栏


def psi_creep(t, ti, fci, V_in3, S_in2, H):
    VS = V_in3 / S_in2
    ks = max(1.45 - 0.13 * VS, 1.0)
    khc = 1.56 - 0.008 * H
    kf = 5 / (1 + fci)
    ktd = t / (12 * (100 - 4 * fci) / (fci + 20) + t)
    return 1.9 * ks * khc * kf * ktd * ti ** (-0.118)


def eps_shink(t, fci, V_in3, S_in2, H):
    VS = V_in3 / S_in2
    ks = max(1.45 - 0.13 * VS, 1.0)
    khc = 2.0 - 0.014 ** H
    kf = 5 / (1 + fci)
    ktd = t / (12 * (100 - 4 * fci) / (fci + 20) + t)
    return ks * khc * kf * ktd * 0.48e-3


if __name__ == "__main__":
    print(beta_RH(0.8))

    print('%.3E' % Sbc)
    print('%.3E' % Stg)
    print('%.3E' % Stc)
