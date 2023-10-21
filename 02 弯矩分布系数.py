import src as ss

S = 3150
ts = 325
Nb = 7
n = ss.Ec / ss.Ec_slab

A = ss.A
I = ss.I
eg = ts * 0.5 + ss.yt
Kg = n * (I + A * eg ** 2)
print("%.3E" % Kg)
L = 45000

MDF = 0.075 + (S / 2900) ** 0.6 * (S / L) ** 0.2 * (Kg / (L * ts ** 3)) ** 0.1
print("%.3f" % MDF)

VDF = 0.2 + (S / 3600) - (S / 10700) ** 2
print("%.3f" % VDF)



S = 2950
ts = 325
Nb = 6
n = ss.Ec / ss.Ec_slab

A = ss.A
I = ss.I
eg = ts * 0.5 + ss.yt
Kg = n * (I + A * eg ** 2)
print("%.3E" % Kg)
L = 45000

MDF = 0.075 + (S / 2900) ** 0.6 * (S / L) ** 0.2 * (Kg / (L * ts ** 3)) ** 0.1
print("%.3f" % MDF)

VDF = 0.2 + (S / 3600) - (S / 10700) ** 2
print("%.3f" % VDF)