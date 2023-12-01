import numpy as np

from src.sections import DXFSection


def principle(sx, tx):
    s1 = sx / 2 + np.sqrt((sx / 2) ** 2 + tx)
    s3 = sx / 2 - np.sqrt((sx / 2) ** 2 + tx)
    return [s1, s3]


S2 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, 225, 1, 7483.1945, 0.1)
S2.addStrand(75, 1395, 14 * 140, )
S2.addStrand(125, 1395, 14 * 140, )
S2.addStrand(175, 1395, 8 * 140, )
S2.addStrand(225, 1395, 2 * 140, )
S2.addStrand(1955, 1395, 4 * 140, )
S2.addTendon(320, 1327, 1 * 12 * 140, 1)
S2.addTendon(440, 1327, 1 * 12 * 140, 2)
S2.addTendon(560, 1327, 1 * 12 * 140, 2)
S2.addTendon(680, 1327, 1 * 12 * 140, 2)

I = S2.cp().I
A = S2.cp().A
M = 5.532e9
N = -1.2e7
F = 1.868e6
ya = S2.cp().yt - 290
s1 = M / I * ya
s0 = N / A
print(s1 + s0)
yz = 629.1758
Az = 551338.226
Sz = Az * (S2.cp().yb - yz)
print(Sz)
tau = F * Sz / (I * 225)
print(tau)
print(principle(s1 + s0, tau))
