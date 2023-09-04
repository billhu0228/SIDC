import ezdxf
from ezdxf.math import ConstructionLine, ConstructionArc, Vec2
import numpy as np


class NU2000(object):
    def __init__(self, idd, name, dxf, ymax, dy=0.1):
        self.id = idd
        self.name = name
        doc = ezdxf.readfile(dxf)
        msp = doc.modelspace()
        lines = msp.query('LINE')
        arcs = msp.query('ARC')
        self.lines = [self.ConsL(li) for li in lines]
        self.arcs = [ar.construction_tool() for ar in arcs]
        self.y_max = ymax

    def get_w(self, z0):
        if z0 > self.y_max or z0 < 0:
            return 0
        else:
            cut = ConstructionLine(Vec2(-10000, z0), Vec2(10000, z0))
            ret1 = [e.intersect(cut) for e in self.lines if e.intersect(cut) is not None]
            ret2 = [e.intersect_line(cut)[0] for e in self.arcs if len(e.intersect_line(cut)) != 0]
            ret = ret1 + ret2
        return ret[0].x * 2

    @staticmethod
    def ConsL(line):
        return ConstructionLine(Vec2(line.dxf.start), Vec2(line.dxf.end))


if __name__ == "__main__":
    S45 = NU2000(1, "S45", 'NU2000.dxf', 2000)
    w = S45.get_w(1947.94)
    print(w * 0.5)
