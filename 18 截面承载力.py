import numpy as np

from src.sections import DXFSection

if __name__ == "__main__":
    S45 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, 225, 1, 7483.1945, 0.1)
    S45.addStrand(75, 1395, 14 * 140, )
    S45.addStrand(125, 1395, 14 * 140, )
    S45.addStrand(175, 1395, 8 * 140, )
    S45.addStrand(225, 1395, 2 * 140, )
    S45.addStrand(1955, 1395, 4 * 140, )
    # S45.addTendon(320, 1327, 1 * 12 * 140, 1)
    # S45.addTendon(440, 1327, 1 * 12 * 140, 2)
    # S45.addTendon(560, 1327, 1 * 12 * 140, 2)
    # S45.addTendon(680, 1327, 1 * 12 * 140, 2)
    # print(S45._N_check(100, 0, -65, -3.0e-3))
    print(S45.get_Mn(-2000e3) * 1e-6 * 0.9)
    print(S45.get_Mn(0) * 1e-6 * 0.9)
    print(S45.get_Mn(100) * 1e-6 * 0.9)

    # P1 = DXFSection(1, "S45", './src/NU2000END.dxf', 2000 + 325, 1, 1, 7483.1945, 0.1)
    # P1.addTendon(325 + 100, 1327, 1 * 12 * 140, 1)
    # P1.addTendon(325 + 220, 1327, 1 * 12 * 140, 2)
    # P1.addTendon(325 + 540, 1327, 1 * 12 * 140, 2)
    # P1.addTendon(325 + 660, 1327, 1 * 12 * 140, 2)
    # P1.addRebar(100,420,10*16*16*np.pi*0.25)
    # # print(S45._N_check(100, 0, -65, -3.0e-3))
    # print(P1.get_Mn(-200e3) * 1e-6 * 0.9)
    # print(P1.get_Mn(0) * 1e-6 * 0.9)
    # print(P1.get_Mn(100) * 1e-6 * 0.9)
