import numpy as np

from src.bridge import StressInfo, GenSection

info_pre = StressInfo(1860 * 0.75, 42 * 140, -633.04, -1269.9543)
info_T1 = StressInfo(967, 1 * 12 * 140, -609.948, -1246.8591)
info_T2 = StressInfo(967, 3 * 12 * 140, -369.948, -1006.8591)

end_info_pre = StressInfo(1860 * 0.75, 28 * 140, -617.7945, -936.2342)
end_info_T1 = StressInfo(967, 1 * 12 * 140, -458.132, -776.5717)
end_info_T2 = StressInfo(967, 3 * 12 * 140, 341.868, 23.4283)

pier_info_pre = StressInfo(1860 * 0.75, 28 * 140, -539.6105, -1176.5216)
pier_info_T1 = StressInfo(1020, 1 * 12 * 140, 410.052, -226.8591)
pier_info_T2 = StressInfo(1020, 3 * 12 * 140, 783.3853, 146.4742)

no_comp = GenSection(721016.60, 7483.1945, 3.7064E+11, 929.95, 1070.05)
comp = GenSection(1508516.6, 10813.1945, 9.3682E+11, 1566.8591, 433.1409, 733.1409)


# ------------------------------------  跨中
fr = 0.97 * np.sqrt(50)

s1 = (comp.pre_stress(-1085.8 * 42 * 140., -1269.9543, -comp.yb)
      + comp.pre_stress(-828.0 * 12 * 140., -1246.8591, -comp.yb)
      + comp.pre_stress(-896.7 * 3 * 12 * 140., -1006.8591, -comp.yb)
      )

Sc = comp.I / comp.yb
Snc = no_comp.I / no_comp.yb

Mdnc = -4475311484.042736
Mdnc += -4641059625.906066
Mdnc += -986632698.6819371

Mcr = max(Sc * (fr + s1) - abs(Mdnc) * (Sc / Snc - 1), Sc * fr)

print(Mcr * 1e-6*1.2, Mcr * 1e-6)
# ------------------------------------  墩顶