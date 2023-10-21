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
        self.strands = []
        self.post_1 = []
        self.post_2 = []
        self.sect_data: dict = {}
        self.ny = self._get_n_strip(dy)
        self.dy = self._get_dy()
        self.U = U  # 7483.1945
        self.UC = self.U + (deck_w + deck_h) * 2 - 2 * 1260.0
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
        dA = np.append(self.sect_data['dA'], b * h)
        ys = np.append(self.sect_data['ys'], self.y_max + 0.5 * h)
        cp_gc = dA.dot(ys) / sum(dA)
        gc_change = cp_gc - self.gc()
        cp_I = self.I(gc_change) + b * h ** 3 / 12.0 + (b * h) * (self.y_max + 0.5 * h - cp_gc) ** 2
        return GenSection(sum(dA), self.UC, cp_I, cp_gc, self.y_max - cp_gc, self.y_max + h - cp_gc)

    def prs(self) -> 'StressInfo':
        As = np.array([a[2] for a in self.strands])
        ys = np.array([a[0] for a in self.strands])
        gcs = As.dot(ys) / sum(As)
        b = self.deck_w
        h = self.deck_h
        dA = np.append(self.sect_data['dA'], b * h)
        ys = np.append(self.sect_data['ys'], self.y_max + 0.5 * h)
        cp_gc = dA.dot(ys) / sum(dA)
        return StressInfo(1860 * 0.75, sum(As), gcs - self.gc(), gcs - cp_gc)

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

    def _N_check(self, NA, Nu, fc, epsu):
        # As = np.array([a[2] for a in self.strands])
        # ys = np.array([a[0] for a in self.strands])
        # gcs = As.dot(ys) / sum(As)
        b = self.deck_w
        h = self.deck_h
        dA = np.append(self.sect_data['dA'], b * h)
        ys = np.append(self.sect_data['ys'], self.y_max + 0.5 * h)
        cp_gc = dA.dot(ys) / sum(dA)
        ys = ys - NA
        a = self.y_max + h - NA
        phi = epsu / a
        eps = ys * phi
        sigma = []
        for y0 in ys:
            if y0 <= 0.25 * a:
                sigma.append(0)
            else:
                sigma.append(0.85 * fc)
        sigma = np.array(sigma)
        Aps = self.prs().data[1]
        epc = NA - (cp_gc + self.prs().data[3])
        epsp = -epc / a * epsu
        fpu = 0.9 * 1860
        fps = max(epsp * 195e3, fpu)
        N = sigma.dot(dA) + Aps * fps
        return Nu - N

    def get_Mn(self, Nu, fc=-65.0, epsu=-3 * 1e-3):
        NA = bisect(self._N_check, 100, self.y_max, (Nu, fc, epsu))
        return NA


if __name__ == "__main__":
    S45 = DXFSection(1, "S45", 'NU2000.dxf', 2000, 300, 3100, 7483.1945, 0.1)
    print(2 * S45.Area() / S45.U)
    print("%.4E" % S45.I())

    S45.addStrand(75, 1860 * 0.9, 8 * 140, )
    S45.addStrand(125, 1860 * 0.9, 8 * 140, )
    S45.addStrand(175, 1860 * 0.9, 6 * 140, )
    S45.addStrand(225, 1860 * 0.9, 2 * 140, )
    S45.addStrand(1955, 1860 * 0.9, 4 * 140, )
    rr = S45.get_Mn(0)
    print(rr)
    m = S45.cp()
# w = S45.get_w(1947.94)
# print(w * 0.5)
