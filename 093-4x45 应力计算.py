import pandas as pd

from src import Superstructure
from src.sections import DXFSection

if __name__ == "__main__":
    Bridge = Superstructure([45, ] * 4, 65.0, 50.0, pr_detail=False)

    Tn1 = 12
    Tn2 = 12
    S0 = DXFSection(0, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945)
    S0.addStrand(75, 1860 * 0.75, 8 * 140, )
    S0.addStrand(125, 1860 * 0.75, 8 * 140, )
    S0.addStrand(175, 1860 * 0.75, 6 * 140, )
    S0.addStrand(225, 1860 * 0.75, 2 * 140, )
    S0.addStrand(1955, 1860 * 0.75, 4 * 140, )
    S0.addTendon(550, 1478, 1 * Tn1 * 140, 1)
    S0.addTendon(950, 1478, 1 * Tn1 * 140, 2)
    S0.addTendon(1350, 1478, 1 * Tn2 * 140, 2)
    S0.addTendon(1750, 1478, 1 * Tn2 * 140, 2)

    S1 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945)
    S1.addStrand(75, 1860 * 0.75, 14 * 140, )
    S1.addStrand(125, 1860 * 0.75, 14 * 140, )
    S1.addStrand(175, 1860 * 0.75, 8 * 140, )
    S1.addStrand(225, 1860 * 0.75, 2 * 140, )
    S1.addStrand(1955, 1860 * 0.75, 4 * 140, )
    S1.addTendon(550, 1468, 1 * Tn1 * 140, 1)
    S1.addTendon(950, 1468, 1 * Tn1 * 140, 2)
    S1.addTendon(1350, 1468, 1 * Tn2 * 140, 2)
    S1.addTendon(1750, 1468, 1 * Tn2 * 140, 2)

    S2 = DXFSection(2, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945)
    S2.addStrand(75, 1860 * 0.75, 14 * 140, )
    S2.addStrand(125, 1860 * 0.75, 14 * 140, )
    S2.addStrand(175, 1860 * 0.75, 8 * 140, )
    S2.addStrand(225, 1860 * 0.75, 2 * 140, )
    S2.addStrand(1955, 1860 * 0.75, 4 * 140, )
    S2.addTendon(320, 1411, 1 * Tn1 * 140, 1)
    S2.addTendon(440, 1411, 1 * Tn1 * 140, 2)
    S2.addTendon(560, 1411, 1 * Tn2 * 140, 2)
    S2.addTendon(680, 1411, 1 * Tn2 * 140, 2)

    S3 = DXFSection(3, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945)
    S3.addStrand(75, 1860 * 0.75, 14 * 140, )
    S3.addStrand(125, 1860 * 0.75, 14 * 140, )
    S3.addStrand(175, 1860 * 0.75, 8 * 140, )
    S3.addStrand(225, 1860 * 0.75, 2 * 140, )
    S3.addStrand(1955, 1860 * 0.75, 4 * 140, )
    S3.addTendon(1340, 1339, 1 * Tn1 * 140, 1)
    S3.addTendon(1460, 1339, 1 * Tn1 * 140, 2)
    S3.addTendon(1780, 1339, 1 * Tn2 * 140, 2)
    S3.addTendon(1900, 1339, 1 * Tn2 * 140, 2)

    S8 = DXFSection(8, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945)
    S8.addStrand(75, 1860 * 0.75, 14 * 140, )
    S8.addStrand(125, 1860 * 0.75, 14 * 140, )
    S8.addStrand(175, 1860 * 0.75, 8 * 140, )
    S8.addStrand(225, 1860 * 0.75, 2 * 140, )
    S8.addStrand(1955, 1860 * 0.75, 4 * 140, )
    S8.addTendon(320, 901, 1 * Tn1 * 140, 1)
    S8.addTendon(440, 901, 1 * Tn1 * 140, 2)
    S8.addTendon(560, 901, 1 * Tn2 * 140, 2)
    S8.addTendon(680, 901, 1 * Tn2 * 140, 2)

    R0 = Bridge.check_stress(0, 0.5, S0, False)
    R1 = Bridge.check_stress(0, 5, S1, False)
    R2 = Bridge.check_stress(0, 22.5, S2, True)
    R3 = Bridge.check_stress(0, 40, S3, False)
    R8 = Bridge.check_stress(3, 22.5, S8, True)

    Result = [R0, R1, R2, R3, R8]
    Result = pd.concat(Result)
    # Result.index=Result.index

    pd.set_option('display.max_columns', None)
    pd.options.display.float_format = '{:,.1f}'.format
    print(Result)
    # Result.to_excel("./res/4x45米应力计算结果.xlsx")
