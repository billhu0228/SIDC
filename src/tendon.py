import numpy as np
import PyAngle
import ezdxf
from ezdxf.math import ConstructionLine, ConstructionArc, Vec2
import pint

Q_ = pint.Quantity
ureg = pint.UnitRegistry()


def getArc(pt0: 'Vec2', pt1: 'Vec2'):
    dy = pt1.y - pt0.y
    dx = pt1.x - pt0.x
    coord = np.sqrt(dx ** 2 + dy ** 2)
    R = 0.5 * coord / dy * coord
    ang = np.arctan(dy / dx)
    ang_deg = PyAngle.Angle.from_rad(ang).to_degrees()
    if dy > 0:
        if dx > 0:
            return ConstructionArc(center=Vec2(pt0.x, pt0.y + R), start_angle=270, end_angle=270 + ang_deg)
        else:
            return ConstructionArc(center=Vec2(pt0.x, pt0.y + R), start_angle=270 - ang_deg, end_angle=270)
    else:
        if dx > 0:
            return ConstructionArc(center=Vec2(pt0.x, pt0.y - R), start_angle=90 - ang_deg, end_angle=90)
        else:
            return ConstructionArc(center=Vec2(pt0.x, pt0.y - R), start_angle=90, end_angle=90 + ang_deg)


class CSCTendon:
    def __init__(self, s1s2, s3, lineA: 'ConstructionLine', lineB: 'ConstructionLine', startY, endY):
        self.elements = []
        self.elements.append(getArc(lineA.start, Vec2(0, startY)))
        self.elements.append(lineA)
        self.elements.append(lineB)
        self.elements.append(getArc(lineB.end, Vec2(s1s2 + s3, endY)))
        self.length = s1s2 + s3

    def getZ(self, x):
        cutline = ezdxf.math.ConstructionLine(Vec2(x, -1), Vec2(x, 10))
        ret = []
        for e in self.elements:
            if type(e) is ConstructionLine:
                r = cutline.intersect(e)
                if type(r) is Vec2:
                    ret.append(r)
            else:
                r = e.intersect_line(cutline)
                if len(r) == 1:
                    ret.append(r[0])
        if len(ret) == 0:
            print(x)
            raise Exception()
        else:
            return ret[0].y

    @property
    def xlist_inch(self):
        xs = list(range(int(np.round(self.length, 0))))
        xs.append(self.length)
        return [Q_(x, ureg.m).to(ureg.inch).m for x in xs]

    @property
    def xlist_m(self):
        xs = list(range(int(np.round(self.length, 0))))
        xs.append(self.length)
        return [x for x in xs]

    @property
    def ylist_m(self):
        return [self.getZ(x) for x in self.xlist_m]

    @property
    def ylist_inch(self):
        ys = self.ylist_m
        return [Q_(y, ureg.m).to(ureg.inch).m for y in ys]

    @property
    def num_points(self):
        return int(np.round(self.length, 0)) + 1

    @property
    def my_type(self):
        return [1, ] + [7, ] * (self.num_points - 2) + [6, ]

    def to_layout(self, layout, dx=0, dy=0):
        for e in self.elements:
            e.translate(dx, dy)
            if type(e) is ConstructionLine:
                layout.add_line(e.start, e.end)
            else:
                e.add_to_layout(layout)

    def to_dxf(self, dxf_file):
        doc = ezdxf.new(dxfversion="R2010")
        msp = doc.modelspace()
        for e in self.elements:
            if type(e) is ConstructionLine:
                msp.add_line(e.start, e.end)
            else:
                e.add_to_layout(msp)
        doc.saveas(dxf_file)


class PME1Tendon:
    def __init__(self, span1, span2, span3,
                 lineA: 'ConstructionLine', lineB: 'ConstructionLine',
                 lineC: 'ConstructionLine', lineD: 'ConstructionLine',
                 arcE: 'ConstructionArc', f1=0.5, f2=0.5):
        self.elemlist = []
        self.elemlist.append(lineA)
        if np.abs(lineA.end.y - lineB.start.y) < 1e-4:
            self.elemlist += [ConstructionLine(lineA.end, lineB.start), ]
        else:
            self.elemlist += self.genArcs(lineA.end, lineB.start, f1)
        self.elemlist.append(lineB)
        self.elemlist += self.genArcs(lineB.end, lineC.start, f2)
        self.elemlist.append(lineC)
        self.elemlist.append(lineD)
        self.elemlist.append(arcE)
        self.Span1 = span1
        self.Span2 = span2
        self.Span3 = span3
        self.length = span1 + span2 + span3
        pass

    @property
    def xlist_inch(self):
        xs = list(range(int(np.round(self.length, 0))))
        xs.append(self.length)
        return [Q_(x, ureg.m).to(ureg.inch).m for x in xs]

    @property
    def xlist_m(self):
        xs = list(range(int(np.round(self.length, 0))))
        xs.append(self.length)
        return [x for x in xs]

    @property
    def ylist_m(self):
        return [self.getZ(x) for x in self.xlist_m]

    @property
    def ylist_inch(self):
        ys = self.ylist_m
        return [Q_(y, ureg.m).to(ureg.inch).m for y in ys]

    @property
    def num_points(self):
        return int(np.round(self.length, 0)) + 1

    @property
    def my_type(self):
        return [1, ] + [7, ] * (self.num_points - 2) + [6, ]

    def to_layout(self, layout, dx=0, dy=0):
        for e in self.elemlist:
            e.translate(dx, dy)
            if type(e) is ConstructionLine:
                layout.add_line(e.start, e.end)
            else:
                e.add_to_layout(layout)

    def to_dxf(self, dxf_file):
        doc = ezdxf.new(dxfversion="R2010")
        msp = doc.modelspace()
        for e in self.elemlist:
            if type(e) is ConstructionLine:
                msp.add_line(e.start, e.end)
            else:
                e.add_to_layout(msp)
        doc.saveas(dxf_file)

    def getZ(self, x):
        if x < 0:
            return self.getZ(0)
        elif x > self.length:
            return self.getZ(self.length)
        else:
            cutline = ezdxf.math.ConstructionLine(Vec2(x, -1), Vec2(x, 10))
            ret = []
            for e in self.elemlist:
                if type(e) is ConstructionLine:
                    r = cutline.intersect(e)
                    if type(r) is Vec2:
                        ret.append(r)
                else:
                    r = e.intersect_line(cutline)
                    if len(r) == 1:
                        ret.append(r[0])
            if len(ret) == 0:
                print(x)
                raise Exception()
            else:
                return ret[0].y

    @staticmethod
    def ArcE(idx, dx=0):
        arcs = [ConstructionArc(center=Vec2(21.1745867, -45.41553859), radius=46.95100059, start_angle=78.8, end_angle=87.77183029),
                ConstructionArc(center=Vec2(15.45384088, -133.59245049), radius=135.50269774, start_angle=83.7, end_angle=86.80753808),
                ConstructionArc(center=Vec2(16.33460460, -211.08247855), radius=213.08674769, start_angle=86.2, end_angle=88.20748254), ]
        arcs[idx].translate(dx, 0)
        return arcs[idx]

    @staticmethod
    def genArcs(P1: 'Vec2', P2: 'Vec2', ratio):
        dy = np.abs(P2.y - P1.y)
        dx = np.abs(P2.x - P1.x)
        rad = np.arctan(dy / dx) * 2
        deg = PyAngle.Angle.from_rad(rad).to_degrees()
        Rsum = dx / np.sin(rad)
        r1 = ratio * Rsum
        r2 = Rsum - r1
        ydir1 = -1 if P2.y < P1.y else 1
        c1 = P1 + Vec2(0, ydir1 * r1)
        c2 = P2 + Vec2(0, -ydir1 * r2)
        if P2.y < P1.y:
            arc1 = ConstructionArc(center=c1, radius=r1, start_angle=90 - deg, end_angle=90)
            arc2 = ConstructionArc(center=c2, radius=r2, start_angle=270 - deg, end_angle=270.0)
        else:
            arc1 = ConstructionArc(center=c1, radius=r1, start_angle=270, end_angle=270 + deg)
            arc2 = ConstructionArc(center=c2, radius=r2, start_angle=90, end_angle=90 + deg)
        return [arc1, arc2]


if __name__ == "__main__":
    v = getArc(Vec2(0, 0), Vec2(-1, -1))
    print(v)
    Sp1 = 4.5
    Sp2 = 15.5
    Sp3 = 10.25
    Dy = 0
    y0 = 0.65
    y1 = 0.2 + Dy
    y2 = 1.5
    La = ConstructionLine(Vec2(0, y0), Vec2(2.0, y0))
    xmid = Sp1 + 0.5 * (Sp2 - 3.5 - 1.75)
    Lb = ConstructionLine(Vec2(xmid - 0.3, y1), Vec2(xmid + 0.3, y1))
    Lc = ConstructionLine(Vec2(Sp1 + Sp2 - 0.44, y2), Vec2(Sp1 + Sp2, y2))
    Ld = ConstructionLine(Vec2(Sp1 + Sp2, y2), Vec2(Sp1 + Sp2 + 3, y2))
    Ae = PME1Tendon.ArcE(0)
    T1 = PME1Tendon(4.5, 15.5, 10.25, La, Lb, Lc, Ld, Ae)
