import numpy as np

from src.sections import DXFSection

if __name__ == "__main__":
    S40 = DXFSection(1, "S45", '../src/NU2000.dxf', 2000, 225, 1400 * 2, 7483.1945, 1)
    S40.addTendon(275, 1327, 1 * 15 * 140, 1)
    S40.addTendon(125, 1327, 3 * 15 * 140, 1)
    phiMn = S40.get_Mn(0) * 1e-6 * 0.9
    print("%i\t%.2f" % (phiMn, phiMn / 20485))

    S33 = DXFSection(1, "S33", '../src/NU2000.dxf', 2000, 225, 1400 * 2, 7483.1945, 1)
    S33.addTendon(275, 1327, 1 * 11 * 140, 1)
    S33.addTendon(125, 1327, 1 * 11 * 140, 1)
    S33.addTendon(125, 1327, 2 * 10 * 140, 1)
    phiMn = S33.get_Mn(0) * 1e-6 * 0.9
    print("%i\t%.2f" % (phiMn, phiMn / 14500))

    # print(S40.get_Mn(100) * 1e-6 * 0.9)

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
