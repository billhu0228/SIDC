import numpy as np

from src.bridge import StressInfo, GenSection
from src.sections import DXFSection

info_pre = StressInfo(1860 * 0.75, 42 * 140, -633.04, -1269.9543)
info_T1 = StressInfo(967, 1 * 12 * 140, -609.948, -1246.8591)
info_T2 = StressInfo(967, 3 * 12 * 140, -369.948, -1006.8591)

end_info_pre = StressInfo(1860 * 0.75, 28 * 140, -617.7945, -936.2342)
end_info_T1 = StressInfo(967, 1 * 12 * 140, -458.132, -776.5717)
end_info_T2 = StressInfo(967, 3 * 12 * 140, 341.868, 23.4283)

pier_info_pre = StressInfo(1860 * 0.75, 28 * 140, -539.6105, -1176.5216)
pier_info_T1 = StressInfo(1020, 1 * 12 * 140, 410.052, -226.8591)
pier_info_T2 = StressInfo(1020, 3 * 12 * 140, 783.3853, 146.4742)

# no_comp = GenSection(721016.60, 7483.1945, 3.7064E+11, 929.95, 1070.05)
# comp = GenSection(1508516.6, 10813.1945, 9.3682E+11, 1566.8591, 433.1409, 733.1409)

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

# ------------------------------------  跨中
fr = 0.97 * np.sqrt(65)
comp = S2.cp()
no_comp = S2.ncp()

s1 = 36.65
Sc = comp.I / comp.yb
print("Scfr=%.0f" % (Sc * fr * 1e-6))
Snc = no_comp.I / no_comp.yb
DW = 1980e6
DC = 10107E6
Mdnc = DW + DC

Mcr = max(Sc * (fr + s1) - abs(Mdnc) * (Sc / Snc - 1), Sc * fr)

print("Mcr=%.0f, 1.2Mcr=%.0f" % (Mcr * 1e-6, 1.2 * Mcr * 1e-6))
# ------------------------------------  墩顶
s1 = 2.7
Sc = comp.I / comp.yt
print("Scfr=%.0f" % (Sc * fr * 1e-6))
Snc = no_comp.I / no_comp.yb
DW = 2605e6
DC = 2049E6
Mdnc = DW + DC

Mcr = max(Sc * (fr + s1) - abs(Mdnc) * (Sc / Snc - 1), Sc * fr)

print("Mcr=%.0f, 1.2Mcr=%.0f" % (Mcr * 1e-6, 1.2 * Mcr * 1e-6))
