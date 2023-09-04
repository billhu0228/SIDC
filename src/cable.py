import numpy as np
import PyAngle
import ezdxf
from ezdxf.math import ConstructionLine, ConstructionArc, Vec2

from src.tendon import PME1Tendon


def PME1Cables(S1=4.5, S2=15.5, S3=10.25):
    dy = 3.1 - 0.2 * S2
    xa = 0.2 + 0.4 * S1
    Sp1 = S1
    Sp2 = S2
    Sp3 = S3
    y0 = 0.65
    y1 = 0.2 + dy
    y2 = 1.5
    La = ConstructionLine(Vec2(0, y0), Vec2(xa, y0))
    xmid = Sp1 + 0.5 * (Sp2 - 3.5 - 1.75)
    Lb = ConstructionLine(Vec2(xmid - 0.3, y1), Vec2(xmid + 0.3, y1))
    Lc = ConstructionLine(Vec2(Sp1 + Sp2 - 0.44, y2), Vec2(Sp1 + Sp2, y2))
    Ld = ConstructionLine(Vec2(Sp1 + Sp2, y2), Vec2(Sp1 + Sp2 + 3, y2))
    Ae = PME1Tendon.ArcE(0, dx=Sp1 + Sp2 + Sp3 - 30.25)
    T1 = PME1Tendon(Sp1, Sp2, Sp3, La, Lb, Lc, Ld, Ae)
    y0 = 1.1
    y1 = 0.4 + dy
    y2 = 1.7
    La = ConstructionLine(Vec2(0, y0), Vec2(xa, y0))
    xmid = Sp1 + 0.5 * (Sp2 - 3.5 - 1.75)
    Lb = ConstructionLine(Vec2(xmid - 0.3, y1), Vec2(xmid + 0.3, y1))
    Lc = ConstructionLine(Vec2(Sp1 + Sp2 - 0.44, y2), Vec2(Sp1 + Sp2, y2))
    Ld = ConstructionLine(Vec2(Sp1 + Sp2, y2), Vec2(Sp1 + Sp2 + 3, y2))
    Ae = PME1Tendon.ArcE(1, dx=Sp1 + Sp2 + Sp3 - 30.25)
    T2 = PME1Tendon(Sp1, Sp2, Sp3, La, Lb, Lc, Ld, Ae)
    y0 = 1.55
    y1 = 0.6 + dy
    y2 = 1.9
    La = ConstructionLine(Vec2(0, y0), Vec2(xa, y0))
    xmid = Sp1 + 0.5 * (Sp2 - 3.5 - 1.75)
    Lb = ConstructionLine(Vec2(xmid - 0.3, y1), Vec2(xmid + 0.3, y1))
    Lc = ConstructionLine(Vec2(Sp1 + Sp2 - 0.44, y2), Vec2(Sp1 + Sp2, y2))
    Ld = ConstructionLine(Vec2(Sp1 + Sp2, y2), Vec2(Sp1 + Sp2 + 3, y2))
    Ae = PME1Tendon.ArcE(2, dx=Sp1 + Sp2 + Sp3 - 30.25)
    T3 = PME1Tendon(Sp1, Sp2, Sp3, La, Lb, Lc, Ld, Ae)
    return [T1, T2, T3]


if __name__ == "__main__":
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()
    vals = [(4.46, 9.59), (2.5, 10.5), (4.5, 10.5), (2.5, 11), (3, 11), (2.5, 11.5),
            (3, 11.5), (3.5, 11.5), (2.1, 12), (2.8, 12), (2.1, 12.75), (2.85, 12.75),
            (4.5, 12.75), ]
    ii = 0
    for ss1, ss2 in vals:
        y00 = -5 * ii
        cables = PME1Cables(ss1, ss2, 10.25)
        for tendon in cables:
            tendon.to_layout(msp, 0, y00)
        ii += 1
    doc.saveas("Tall.dxf")
    f = 1
