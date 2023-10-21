import numpy as np

aeff = 0.88 * 170
beff = 0.88 * 170
s = 400
K = 1
Pu = 0.8 * 1860 * 140 * 12
Ab = np.pi * (170 * 0.5) ** 2

lc = 1.15 * aeff
t = 1010

ft = lc * (1 / (beff - (1 / t)))
print(ft)

fca = (0.6 * Pu * K) / (Ab * (1 + ft))
print(fca)