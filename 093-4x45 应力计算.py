import pandas as pd

from src import Superstructure
from src.sections import DXFSection

if __name__ == "__main__":
    Bridge = Superstructure([45, ] * 4, 65.0, 50.0, pr_detail=True)
    pre_stressing = 1860 * 0.75 * 0.92
    EffW = 3100
    DeckH = 225
    Tn1 = 16
    Tn2 = 16
    S0 = DXFSection(0, "S45", './src/NU2000.dxf', 2000, DeckH, EffW, 7483.1945)
    S0.addStrand(75, pre_stressing, 8 * 140, )
    S0.addStrand(125, pre_stressing, 8 * 140, )
    S0.addStrand(175, pre_stressing, 6 * 140, )
    S0.addStrand(225, pre_stressing, 2 * 140, )
    S0.addStrand(1955, pre_stressing, 4 * 140, )
    S0.addTendon(550, 1395, 1 * Tn1 * 140, 1)
    S0.addTendon(950, 1395, 1 * Tn1 * 140, 2)
    S0.addTendon(1350, 1395, 1 * Tn2 * 140, 2)
    S0.addTendon(1750, 1395, 1 * Tn2 * 140, 2)

    S1 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, DeckH, EffW, 7483.1945)
    S1.addStrand(75, pre_stressing, 14 * 140, )
    S1.addStrand(125, pre_stressing, 14 * 140, )
    S1.addStrand(175, pre_stressing, 8 * 140, )
    S1.addStrand(225, pre_stressing, 2 * 140, )
    S1.addStrand(1955, pre_stressing, 4 * 140, )
    S1.addTendon(550, 1383, 1 * Tn1 * 140, 1)
    S1.addTendon(950, 1383, 1 * Tn1 * 140, 2)
    S1.addTendon(1350, 1383, 1 * Tn2 * 140, 2)
    S1.addTendon(1750, 1383, 1 * Tn2 * 140, 2)

    S2 = DXFSection(2, "S45", './src/NU2000.dxf', 2000, DeckH, EffW, 7483.1945)
    S2.addStrand(75, pre_stressing, 14 * 140, )
    S2.addStrand(125, pre_stressing, 14 * 140, )
    S2.addStrand(175, pre_stressing, 8 * 140, )
    S2.addStrand(225, pre_stressing, 2 * 140, )
    S2.addStrand(1955, pre_stressing, 4 * 140, )
    S2.addTendon(320, 1327, 1 * Tn1 * 140, 1)
    S2.addTendon(440, 1327, 1 * Tn1 * 140, 2)
    S2.addTendon(560, 1327, 1 * Tn2 * 140, 2)
    S2.addTendon(680, 1327, 1 * Tn2 * 140, 2)

    S3 = DXFSection(3, "S45", './src/NU2000.dxf', 2000, DeckH, EffW, 7483.1945)
    S3.addStrand(75, pre_stressing, 14 * 140, )
    S3.addStrand(125, pre_stressing, 14 * 140, )
    S3.addStrand(175, pre_stressing, 8 * 140, )
    S3.addStrand(225, pre_stressing, 2 * 140, )
    S3.addStrand(1955, pre_stressing, 4 * 140, )
    S3.addTendon(1340, 1262, 1 * Tn1 * 140, 1)
    S3.addTendon(1460, 1262, 1 * Tn1 * 140, 2)
    S3.addTendon(1780, 1262, 1 * Tn2 * 140, 2)
    S3.addTendon(1900, 1262, 1 * Tn2 * 140, 2)

    S8 = DXFSection(8, "S45", './src/NU2000.dxf', 2000, DeckH, EffW, 7483.1945)
    S8.addStrand(75, pre_stressing, 14 * 140, )
    S8.addStrand(125, pre_stressing, 14 * 140, )
    S8.addStrand(175, pre_stressing, 8 * 140, )
    S8.addStrand(225, pre_stressing, 2 * 140, )
    S8.addStrand(1955, pre_stressing, 4 * 140, )
    S8.addTendon(320, 850, 1 * Tn1 * 140, 1)
    S8.addTendon(440, 850, 1 * Tn1 * 140, 2)
    S8.addTendon(560, 850, 1 * Tn2 * 140, 2)
    S8.addTendon(680, 850, 1 * Tn2 * 140, 2)

    R0 = Bridge.check_stress(0, 0.5, S0, False)
    R1 = Bridge.check_stress(0, 5, S1, False)
    R2 = Bridge.check_stress(0, 22.5, S2, True)
    R3 = Bridge.check_stress(0, 40, S3, False)
    R8 = Bridge.check_stress(3, 22.5, S8, True)

    # Result = [R2]
    Result = [R0, R1, R2, R3, R8]
    Result = pd.concat(Result)
    Result.index=Result.index

    pd.set_option('display.max_columns', None)
    pd.options.display.float_format = '{:,.1f}'.format
    print(Result)
    Result.to_excel("./res/4x45米应力计算结果.xlsx")
