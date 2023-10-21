import ezdxf
import numpy as np
from ezdxf.math import ConstructionLine, Vec2
from src.units import MPA

fc = 65.0
fc_slab = 50
fci = fc * 0.8
gc = 2250 + 2.29 * fc
Ec = 0.041 * 1 * gc ** 1.5 * np.sqrt(fc)
Eci = 0.041 * 1 * gc ** 1.5 * np.sqrt(fci)
Ec_slab = 0.041 * 1 * gc ** 1.5 * np.sqrt(fc_slab)
n = Ec_slab / Ec

A = 721016.600
h = 2000.0
I = 3.7064E+11
yb = 929.95
yt = 1070.05
Sb = I / yb
St = I / yt

Ac = 1572516.600
hc = 2325.0
Ic = 9.71258953E+11
ybc = 1597.36
ytg = 402.64
ytc = 727.64
Sbc = Ic / ybc
Stg = Ic / ytg
Stc = Ic / ytc

BeamDC = 2500 * 1e-9 * 9.806 * A
DeckDC = 2500 * 1e-9 * 9.806 * 325 * 3100
BarrDC = 2500 * 1e-9 * 9.806 * (2 * 345814.54 + 363302.64) / 7  # 护栏
DW = 2400 * 1e-9 * 9.806 * (120 * 22850) / 7  # 护栏

if __name__ == "__main__":
    print(DW)

    print('%.3E' % Sbc)
    print('%.3E' % Stg)
    print('%.3E' % Stc)
