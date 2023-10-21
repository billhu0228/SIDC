import pandas as pd

from src import Superstructure
from src.sections import DXFSection

if __name__ == "__main__":
    Bridge = Superstructure([45, ] * 5, 65.0, 50.0, pr_detail=True)

    S1 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945, 0.1)
    S1.addStrand(75, 1860 * 0.75, 8 * 140, )
    S1.addStrand(125, 1860 * 0.75, 8 * 140, )
    S1.addStrand(175, 1860 * 0.75, 6 * 140, )
    S1.addStrand(225, 1860 * 0.75, 2 * 140, )
    S1.addStrand(1955, 1860 * 0.75, 4 * 140, )
    S1.addTendon(550, 1487, 1 * 8 * 140, 1)
    S1.addTendon(950, 1487, 1 * 8 * 140, 1)
    S1.addTendon(1350, 1487, 1 * 8 * 140, 2)
    S1.addTendon(1750, 1487, 1 * 8 * 140, 2)

    S2 = DXFSection(2, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945, 0.1)
    S2.addStrand(75, 1860 * 0.75, 14 * 140, )
    S2.addStrand(125, 1860 * 0.75, 14 * 140, )
    S2.addStrand(175, 1860 * 0.75, 8 * 140, )
    S2.addStrand(225, 1860 * 0.75, 2 * 140, )
    S2.addStrand(1955, 1860 * 0.75, 4 * 140, )
    S2.addTendon(320, 1082, 1 * 8 * 140, 1)
    S2.addTendon(440, 1082, 1 * 8 * 140, 1)
    S2.addTendon(560, 1082, 1 * 8 * 140, 2)
    S2.addTendon(680, 1082, 1 * 8 * 140, 2)
    #
    S3 = DXFSection(1, "S45", './src/NU2000.dxf', 2000, 300, 3100, 7483.1945, 0.1)
    S3.addStrand(75, 1860 * 0.75, 8 * 140, )
    S3.addStrand(125, 1860 * 0.75, 8 * 140, )
    S3.addStrand(175, 1860 * 0.75, 6 * 140, )
    S3.addStrand(225, 1860 * 0.75, 2 * 140, )
    S3.addStrand(1955, 1860 * 0.75, 4 * 140, )
    S3.addTendon(1340, 1475, 1 * 8 * 140, 1)
    S3.addTendon(1460, 1475, 1 * 8 * 140, 1)
    S3.addTendon(1780, 1475, 1 * 8 * 140, 2)
    S3.addTendon(1900, 1475, 1 * 8 * 140, 2)
    #
    R1 = Bridge.check_stress(0, 0.2, S1, False)
    R2 = Bridge.check_stress(0, 22.5, S2, True)
    R3 = Bridge.check_stress(0, 44.5, S3, False)

    # Result = [R3, ]
    Result = [R1, R2, R3, ]
    Result = pd.concat(Result)

    pd.set_option('display.max_columns', None)
    pd.options.display.float_format = '{:,.1f}'.format
    print(Result)
    # Result.to_excel("./res/5x45米应力计算结果.xlsx")
#
