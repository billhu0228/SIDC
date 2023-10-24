import pandas as pd

from src import Superstructure
from src.sections import DXFSection

if __name__ == "__main__":
    Bridge = Superstructure([45, ] * 5, 65.0, 50.0, pr_detail=False)
    pre_stressing = 1860 * 0.75 * 0.92
    EffW = 3100
    DeckH = 225

    S1 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, DeckH, EffW, 7483.1945, 0.1)
    S1.addStrand(75, pre_stressing, 8 * 140, )
    S1.addStrand(125, pre_stressing, 8 * 140, )
    S1.addStrand(175, pre_stressing, 6 * 140, )
    S1.addStrand(225, pre_stressing, 2 * 140, )
    S1.addStrand(1955, pre_stressing, 4 * 140, )
    S1.addTendon(550,  1395, 1 * 12 * 140, 1)
    S1.addTendon(950,  1395, 1 * 12 * 140, 2)
    S1.addTendon(1350, 1395, 1 * 12 * 140, 2)
    S1.addTendon(1750, 1395, 1 * 12 * 140, 2)

    S2 = DXFSection(2, "S45", './src/NU2000.dxf', 2000, DeckH, EffW, 7483.1945, 0.1)
    S2.addStrand(75, pre_stressing, 14 * 140, )
    S2.addStrand(125, pre_stressing, 14 * 140, )
    S2.addStrand(175, pre_stressing, 8 * 140, )
    S2.addStrand(225, pre_stressing, 2 * 140, )
    S2.addStrand(1955, pre_stressing, 4 * 140, )
    S2.addTendon(320, 1330, 1 * 12 * 140, 1)
    S2.addTendon(440, 1330, 1 * 12 * 140, 2)
    S2.addTendon(560, 1330, 1 * 12 * 140, 2)
    S2.addTendon(680, 1330, 1 * 12 * 140, 2)
    #
    S3 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, DeckH, EffW, 7483.1945, 0.1)
    S3.addStrand(75, pre_stressing, 8 * 140, )
    S3.addStrand(125, pre_stressing, 8 * 140, )
    S3.addStrand(175, pre_stressing, 6 * 140, )
    S3.addStrand(225, pre_stressing, 2 * 140, )
    S3.addStrand(1955, pre_stressing, 4 * 140, )
    S3.addTendon(1340, 1248, 1 * 12 * 140, 1)
    S3.addTendon(1460, 1248, 1 * 12 * 140, 2)
    S3.addTendon(1780, 1248, 1 * 12 * 140, 2)
    S3.addTendon(1900, 1248, 1 * 12 * 140, 2)
    #
    R1 = Bridge.check_stress(0, 0.5, S1, False)
    R2 = Bridge.check_stress(0, 22.5, S2, True)
    R3 = Bridge.check_stress(0, 44.5, S3, False)

    # Result = [R3, ]
    Result = [R1, R2, R3, ]
    Result = pd.concat(Result)

    pd.set_option('display.max_columns', None)
    pd.options.display.float_format = '{:,.1f}'.format
    print(Result)
    Result.to_excel("./res/5x45米应力计算结果.xlsx")
#
