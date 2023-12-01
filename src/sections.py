import ezdxf
from ezdxf.math import ConstructionLine, ConstructionArc, Vec2
import numpy as np
from scipy.optimize import bisect

from src import GenSection
from src.bridge import StressInfo


class DXFSection(object):
    def __init__(self, idd, name, dxf, ymax, deck_h, deck_w, U, dy: float = 0.1):
        self.id = idd
        self.name = name
        doc = ezdxf.readfile(dxf)
        msp = doc.modelspace()
        lines = msp.query('LINE')
        arcs = msp.query('ARC')
        self.lines = [self.ConsL(li) for li in lines]
        self.arcs = [ar.construction_tool() for ar in arcs]
        self.y_max = ymax
        self.rebar = []
        self.strands = []
        self.post_1 = []
        self.post_2 = []
        self.sect_data: dict = {}
        self.ny = self._get_n_strip(dy)
        self.dy = self._get_dy()
        self.U = U  # 7483.1945
        self.UC = self.U + deck_w * 2 - 2 * 1260.0
        self.sect_data['ys'] = self._get_ys()
        self.sect_data['ws'] = self._get_ws()
        self.sect_data['dA'] = self._get_dA()
        self.deck_h = deck_h
        self.deck_w = deck_w

    def get_w(self, z0):
        if z0 > self.y_max or z0 < 0:
            return 0
        else:
            cut = ConstructionLine(Vec2(-10000, z0), Vec2(10000, z0))
            ret1 = [e.intersect(cut) for e in self.lines if e.intersect(cut) is not None]
            ret2 = [e.intersect_line(cut)[0] for e in self.arcs if len(e.intersect_line(cut)) != 0]
            ret = ret1 + ret2
        return ret[0].x * 2

    def addRebar(self, z0, fy, As):
        self.rebar.append([z0, fy, As])

    def addStrand(self, z0, fy, As):
        self.strands.append([z0, fy, As])

    def addTendon(self, z0, fy, As, order):
        if order == 1:
            self.post_1.append([z0, fy, As])
        else:
            self.post_2.append([z0, fy, As])
        pass

    def _get_n_strip(self, dy_approx) -> int:
        ny = int(self.y_max / dy_approx)
        return ny

    def _get_dy(self) -> float:
        dyy = self.y_max / self.ny
        return dyy

    def _get_ys(self):
        dy = self.dy
        ny = self.ny
        ylist = np.linspace(0 + 0.5 * dy, self.y_max - 0.5 * dy, ny)
        return ylist

    def _get_ws(self):
        ylist = self.sect_data['ys']
        return np.array([self.get_w(y) for y in ylist])

    def _get_dA(self):
        return self.sect_data['ws'] * self.dy

    def Area(self):
        return sum(self.sect_data['dA'])

    def gc(self):
        return (self.sect_data['dA']).dot(self.sect_data['ys']) / self.Area()

    def I(self, yy=0.0):
        dy = self.dy
        dA = self.sect_data['dA']
        ys = self.sect_data['ys'] - (self.gc() + yy)
        ws = self.sect_data['ws']
        dI = ws * dy ** 3 / 12.0 + dA * ys ** 2
        return sum(dI)

    def ncp(self):
        return GenSection(self.Area(), self.U, self.I(), self.gc(), self.y_max - self.gc())

    def cp(self):
        b = self.deck_w
        h = self.deck_h
        dy = [self.dy, ] * len(self.sect_data['dA']) + [100, h]
        dy = np.array(dy)
        dA = np.append(self.sect_data['dA'], [1260 * 100.0, b * h])
        ys = np.append(self.sect_data['ys'], [self.y_max + 50.0, self.y_max + 100 + 0.5 * h])
        ws = np.append(self.sect_data['ws'], [1260, b])
        cp_gc = dA.dot(ys) / sum(dA)
        yscp = ys - cp_gc
        dI = ws * dy ** 3 / 12.0 + dA * yscp ** 2
        cp_I = sum(dI)
        return GenSection(sum(dA), self.UC, cp_I, cp_gc, self.y_max - cp_gc, self.y_max + 100 + h - cp_gc)

    def bar(self):
        As = np.array([a[2] for a in self.rebar])
        ys = np.array([a[0] for a in self.rebar])
        gcs = As.dot(ys) / sum(As)
        b = self.deck_w
        h = self.deck_h
        dA = np.append(self.sect_data['dA'], b * h)
        ys = np.append(self.sect_data['ys'], self.y_max + 0.5 * h)
        cp_gc = dA.dot(ys) / sum(dA)
        return StressInfo(self.rebar[0][1], sum(As), gcs - self.gc(), gcs - cp_gc)

    def prs(self) -> 'StressInfo':
        if len(self.strands) == 0:
            return StressInfo(0, 0, 0, 0)
        else:
            As = np.array([a[2] for a in self.strands])
            ys = np.array([a[0] for a in self.strands])
            gcs = As.dot(ys) / sum(As)
            b = self.deck_w
            h = self.deck_h
            dA = np.append(self.sect_data['dA'], b * h)
            ys = np.append(self.sect_data['ys'], self.y_max + 0.5 * h)
            cp_gc = dA.dot(ys) / sum(dA)
            return StressInfo(self.strands[0][1], sum(As), gcs - self.gc(), gcs - cp_gc)

    def pos(self, order: int) -> 'StressInfo':
        if order == 1:
            data = self.post_1
        else:
            data = self.post_2
        As = np.array([a[2] for a in data])
        ys = np.array([a[0] for a in data])
        gcs = As.dot(ys) / sum(As)
        b = self.deck_w
        h = self.deck_h
        dA = np.append(self.sect_data['dA'], b * h)
        ys = np.append(self.sect_data['ys'], self.y_max + 0.5 * h)
        cp_gc = dA.dot(ys) / sum(dA)
        return StressInfo(data[0][1], sum(As), gcs - self.gc(), gcs - cp_gc)

    @staticmethod
    def ConsL(line):
        return ConstructionLine(Vec2(line.dxf.start), Vec2(line.dxf.end))

    @staticmethod
    def _get_fs(es):
        fs = 195e3 * es
        if abs(fs) > 0.9 * 1860.0:
            return np.sign(fs) * 0.9 * 1860
        else:
            return fs

    @staticmethod
    def _get_fy(es):
        fs = 200e3 * es
        if abs(fs) > 420.0:
            return np.sign(fs) * 420.0
        else:
            return fs

    def _N_check(self, NA, Nu, fc, epsu):
        b = self.deck_w
        h = self.deck_h
        dy = [self.dy, ] * len(self.sect_data['dA']) + [100, h]
        dy = np.array(dy)
        dA = np.append(self.sect_data['dA'], [1260 * 100.0, b * h])
        ys = np.append(self.sect_data['ys'], [self.y_max + 50.0, self.y_max + 100 + 0.5 * h])
        ws = np.append(self.sect_data['ws'], [1260, b])
        cp_gc = dA.dot(ys) / sum(dA)
        yscp = ys - cp_gc
        dI = ws * dy ** 3 / 12.0 + dA * yscp ** 2
        cp_I = sum(dI)

        ys = ys - NA
        a = self.y_max + 100 + h - NA
        if a > 0:
            phi = epsu / -a
        else:
            phi = .0
        sigma = []
        for y0 in ys:
            if y0 <= 0.25 * a:
                sigma.append(0)
            else:
                sigma.append(0.85 * fc)
        sigma = np.array(sigma)

        fpu = 0.9 * 1860
        As = self.bar().data[1]
        ec = NA - (cp_gc + self.bar().data[3])
        esp = phi * ec
        fs = self._get_fy(esp)


        Aps = self.prs().data[1]
        epc = NA - (cp_gc + self.prs().data[3])
        epsp = phi * epc
        fps = self._get_fs(epsp)

        ApsT1 = self.pos(1).data[1]
        epcT1 = NA - (cp_gc + self.pos(1).data[3])
        epspT1 = phi * epcT1
        fpsT1 = self._get_fs(epspT1)

        ApsT2 = self.pos(2).data[1]
        epcT2 = NA - (cp_gc + self.pos(2).data[3])
        epspT2 = phi * epcT2
        fpsT2 = self._get_fs(epspT2)

        N = [sigma.dot(dA),As * fs, Aps * fps, ApsT1 * fpsT1, ApsT2 * fpsT2]
        SN = sum(N)
        return SN - Nu

    def get_Mn(self, Nu, fc=-65.0, epsu=-3 * 1e-3):
        NA = bisect(self._N_check, 1, 2200, (Nu, fc, epsu))
        b = self.deck_w
        h = self.deck_h
        dy = [self.dy, ] * len(self.sect_data['dA']) + [100, h]
        dy = np.array(dy)
        dA = np.append(self.sect_data['dA'], [1260 * 100.0, b * h])
        ys = np.append(self.sect_data['ys'], [self.y_max + 50.0, self.y_max + 100 + 0.5 * h])
        ws = np.append(self.sect_data['ws'], [1260, b])
        cp_gc = dA.dot(ys) / sum(dA)
        yscp = ys - cp_gc
        dI = ws * dy ** 3 / 12.0 + dA * yscp ** 2
        cp_I = sum(dI)
        ys = ys - NA
        a = self.y_max + 100 + h - NA
        if a > 0:
            phi = epsu / -a
        else:
            phi = .0
        sigma = []
        for y0 in ys:
            if y0 <= 0.25 * a:
                sigma.append(0)
            else:
                sigma.append(0.85 * fc)
        sigma = np.array(sigma)

        fpu = 0.9 * 1860
        As = self.bar().data[1]
        ec = NA - (cp_gc + self.bar().data[3])
        esp = phi * ec
        fs = self._get_fy(esp)

        Aps = self.prs().data[1]
        epc = NA - (cp_gc + self.prs().data[3])
        epsp = phi * epc
        fps = self._get_fs(epsp)

        ApsT1 = self.pos(1).data[1]
        epcT1 = NA - (cp_gc + self.pos(1).data[3])
        epspT1 = phi * epcT1
        fpsT1 = self._get_fs(epspT1)

        ApsT2 = self.pos(2).data[1]
        epcT2 = NA - (cp_gc + self.pos(2).data[3])
        epspT2 = phi * epcT2
        fpsT2 = self._get_fs(epspT2)

        N = [sigma.dot(dA), As * fs, Aps * fps, ApsT1 * fpsT1, ApsT2 * fpsT2]
        M = [sum(sigma * dA * -ys),As * fs * ec, Aps * fps * epc, ApsT1 * fpsT1 * epcT1, ApsT2 * fpsT2 * epcT2]
        return sum(M)


if __name__ == "__main__":
    S45 = DXFSection(1, "S45", 'NU2000.dxf', 2000, 225, 3100, 7483.1945, 0.1)
    S45.addStrand(75, 1395, 14 * 140, )
    S45.addStrand(125, 1395, 14 * 140, )
    S45.addStrand(175, 1395, 8 * 140, )
    S45.addStrand(225, 1395, 2 * 140, )
    S45.addStrand(1955, 1395, 4 * 140, )
    S45.addTendon(320, 1327, 1 * 12 * 140, 1)
    S45.addTendon(440, 1327, 1 * 12 * 140, 2)
    S45.addTendon(560, 1327, 1 * 12 * 140, 2)
    S45.addTendon(680, 1327, 1 * 12 * 140, 2)
    # print(S45._N_check(100, 0, -65, -3.0e-3))
    print(S45.get_Mn(-2000e3) * 1e-6)
    print(S45.get_Mn(0) * 1e-6)
    print(S45.get_Mn(100) * 1e-6)
    # print(2 * S45.Area() / S45.U)
    # print("%.4E" % S45.I())

    # S45.addStrand(75, 1860 * 0.9, 8 * 140, )
    # S45.addStrand(125, 1860 * 0.9, 8 * 140, )
    # S45.addStrand(175, 1860 * 0.9, 6 * 140, )
    # S45.addStrand(225, 1860 * 0.9, 2 * 140, )
    # S45.addStrand(1955, 1860 * 0.9, 4 * 140, )
    # rr = S45.get_Mn(0)
    # print(rr)
    # m = S45.cp()
# w = S45.get_w(1947.94)
# print(w * 0.5)
