import numpy as np

import src as ss
from src.sections import DXFSection

S3 = DXFSection(3, "S45", './src/NU2000.dxf', 2000, 225, 3100, 7483.1945)

fc = 65.0
fc_slab = 50
fci = fc * 0.8
gc = 2250 + 2.29 * fc
Ec = 0.041 * 1 * gc ** 1.5 * np.sqrt(fc)
Eci = 0.041 * 1 * gc ** 1.5 * np.sqrt(fci)
Ec_slab = 0.041 * 1 * gc ** 1.5 * np.sqrt(fc_slab)

S = 3100
ts = 265
Nb = 7
n = Ec / Ec_slab

A = S3.Area()
I = S3.I()
eg = 1257.7
Kg = n * (I + A * eg ** 2)
print("%.3E" % Kg)
L = 45000

MDF = 0.075 + (S / 2900) ** 0.6 * (S / L) ** 0.2 * (Kg / (L * ts ** 3)) ** 0.1
print("%.3f" % MDF)

VDF = 0.2 + (S / 3600) - (S / 10700) ** 2
print("%.3f" % VDF)

S = 2950
ts = 265
Nb = 6
n = Ec / Ec_slab
A = S3.Area()
I = S3.I()
eg = 1257.7
Kg = n * (I + A * eg ** 2)
print("%.3E" % Kg)
L = 45000

MDF = 0.075 + (S / 2900) ** 0.6 * (S / L) ** 0.2 * (Kg / (L * ts ** 3)) ** 0.1
print("%.3f" % MDF)

VDF = 0.2 + (S / 3600) - (S / 10700) ** 2
print("%.3f" % VDF)
