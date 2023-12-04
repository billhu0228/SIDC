import ezdxf
from srbpy import Align
from ezdxf.math import Vec2, Vec3, ConstructionLine

connect = [
    ['B1', 409, 408, 407],
    ['B1', 412, 411, 410],
    ['B1', 415, 414, 413],
    ['B1', 212, 213, 214],
    ['B1', 211, 210, 209],

    ['B2', 509, 508, 507],
    ['B2', 516, 517, 518],
    ['B2', 515, 514, 513],
    ['B2', 512, 511, 510],

    ['B3', 406, 405, 404, ],
    ['B3', 403, 402, 401, ],

    ['B4', 204, 203, 202, 201],
    ['B4', 208, 207, 206, 205],
    ['B5', 505, 506, 301, ],
    ['B5', 501, 502, 101, ],
    ['B5', 503, 504, 102, ],
    ['B6', 304],
    ['B6', 303],
    ['B6', 302],
    ['B6', 103],
    ['B6', 104],
    ['B6', 105],
]


class Beam:
    def __init__(self, st: Vec3, ed: Vec3, lineType: str, align_st: Align, align_ed: Align, nd_base: int):
        p0z = self.get_z(st.x, st.y, align_st)
        p1z = self.get_z(ed.x, ed.y, align_ed)
        p0 = Vec3(st.x, st.y, p0z)
        p1 = Vec3(ed.x, ed.y, p1z)
        self.line = (p0, p1)
        self.beam_type = lineType
        self.align_st = align_st
        self.align_ed = align_ed
        self.n0 = nd_base
        self.nlist = []
        self.elist = []
        self.hdr = []
        self.lnr = []

    def get_z(self, x, y, cl: Align):
        st = cl.get_station_by_point(x, y)
        ele = cl.get_elevation(st)
        cc = Vec2(*cl.get_coordinate(st))
        pt = Vec2(x, y)
        dist = cc.distance(pt)
        assert dist <= 15
        cp = cl.get_cross_slope(st)
        lr = cl.get_side(x, y)
        if lr == 0:
            return ele
        elif lr < 0:
            return ele - cp[0] * dist
        else:
            return ele + cp[1] * dist

    def get_location(self, beam_id):
        for e in connect:
            if e.__contains__(beam_id):
                theB = e[0]
                part = [a for a in connect if a[0] == theB]
                return e.index(beam_id), e, part.index(e)
        return None

    def make_nodes_no_use(self):
        wc = Vec3(571278.7841413167, 785624.6223043363, 0)
        pts = self.get_pts()
        n0 = self.n0
        beam_id = int(n0 / 100)
        for pt in pts:
            pp = pt - wc
            self.nlist.append([n0, pp.x, pp.y, pp.z])
            n0 += 1
        e0 = self.n0
        for e in range(len(pts) - 1):
            if self.beam_type.__contains__("DE"):
                if e == len(pts) - 2:
                    secn = 2
                else:
                    secn = 3
            elif self.beam_type.__contains__("AA"):
                if e == 0:
                    secn = 2
                else:
                    secn = 3
            elif self.beam_type.__contains__("SS"):
                if e == 0 or e == (len(pts) - 2):
                    secn = 2
                else:
                    secn = 3
            else:
                secn = 3
            self.elist.append([e0, 1, secn, e0, e0 + 1])
            e0 += 1

    def make_nodes(self):
        wc = Vec3(571278.7841413167, 785624.6223043363, 0)
        pts = self.get_pts()
        n0 = self.n0
        beam_id = int(n0 / 100)
        if beam_id == 409:
            debug = True
        for pt in pts:
            pp = pt - wc
            self.nlist.append([n0, pp.x, pp.y, pp.z])
            n0 += 1
        e0 = self.n0
        for e in range(len(pts) - 1):
            if self.beam_type.__contains__("DE"):
                if e == len(pts) - 2:
                    secn = 2
                else:
                    secn = 3
            elif self.beam_type.__contains__("AA"):
                if e == 0:
                    secn = 2
                else:
                    secn = 3
            elif self.beam_type.__contains__("SS"):
                if e == 0 or e == (len(pts) - 2):
                    secn = 2
                else:
                    secn = 3
            else:
                secn = 3
            self.elist.append([e0, 1, secn, e0, e0 + 1])
            e0 += 1
        loc, blist, trans_loc = self.get_location(beam_id)
        if loc > 1:
            dirX = (Vec3(self.nlist[-1][1:]) - Vec3(self.nlist[-2][1:])).normalize()
            p0 = Vec3(self.nlist[-1][1:]) + dirX * 0.25
            self.nlist.append([n0, p0.x, p0.y, p0.z])
            n0 += 1
            self.elist.append([e0, 1, 4, e0, e0 + 1])
            e0 += 1
            self.elist.append([e0, 1, 4, e0, blist[loc - 1] * 100])
            e0 += 1
        if trans_loc > 0:
            part = [a for a in connect if a[0] == blist[0]]
            next = part[trans_loc - 1][loc]
            pts = n0 % 100
            if self.beam_type.__contains__("MM"):
                sec_list = [None, ] + [5, ] * (pts - 3) + [None, ] + [6, ]
            elif self.beam_type.__contains__("DE"):
                sec_list = [None, ] + [5, ] * (pts - 3) + [6, ] + [None, ]
            else:
                sec_list = [None, ] + [6, ] + [5, ] * (pts - 4) + [None, ] + [6, ]
            for nn in range(pts):
                if sec_list[nn] is not None:
                    self.elist.append([e0, 1, sec_list[nn], beam_id * 100 + nn, next * 100 + nn])
                    e0 += 1
        if self.beam_type.__contains__("DE"):
            p0 = Vec3(self.nlist[-1][1:])
            self.hdr.append([n0, p0.x, p0.y, p0.z - 0.3, self.nlist[-1][0]])
            n0 += 1
        elif self.beam_type.__contains__("MM"):
            p0 = Vec3(self.nlist[-1][1:])
            self.hdr.append([n0, p0.x, p0.y, p0.z - 0.3, self.nlist[-1][0]])
            n0 += 1
        else:
            p0 = Vec3(self.nlist[-1][1:])
            self.hdr.append([n0, p0.x, p0.y, p0.z - 0.3, self.nlist[-1][0]])
            n0 += 1
            p0 = Vec3(self.nlist[0][1:])
            self.hdr.append([n0, p0.x, p0.y, p0.z - 0.3, self.nlist[0][0]])
            n0 += 1

    def get_pts(self):
        st = self.line[0]
        ed = self.line[1]
        dd = (ed - st).normalize()
        length = (ed - st).magnitude
        nn = 4 if length > 38 else 2
        x0 = (length - nn * 7.5) * 0.5
        try:
            assert x0 > 5
        except AssertionError:
            f = 1
        res = [st, ]
        for n in range(nn + 1):
            res.append(st + dd * (x0 + 7.5 * n))
        res.append(ed)
        if self.beam_type.__contains__("DE"):
            res.append(st + dd * 0.8)
        elif self.beam_type.__contains__("AA"):
            res.append(ed - dd * 0.8)
        elif self.beam_type.__contains__("SS"):
            res.append(st + dd * 0.8)
            res.append(ed - dd * 0.8)
        res.sort(key=lambda p: p.x)
        return res


if __name__ == '__main__':
    D1 = Align('D1', './Data/EI/D1')
    D2 = Align('D2', './Data/EI/D2')
    D3 = Align('D3', './Data/EI/D3')
    D4 = Align('D4', './Data/EI/D4')
    M = Align('M', './Data/EI/M')
    Ramps = [D1, D2, D3, D4, M]
    dxf = ['R1', 'R2', 'R3', 'R4', 'M']
    Beams = []
    for i in range(5):
        doc = ezdxf.readfile(r".\Data\%s.dxf" % dxf[i])
        j = 1
        for e in doc.modelspace():
            pts = [e.dxf.start, e.dxf.end]
            pts.sort(key=lambda A: A.x)
            if dxf[i] in ['R1', 'R3']:
                if pts[0].x > 571177.1567:
                    raise ValueError
                elif pts[1].x > 571177.1567:
                    b = Beam(pts[1], pts[0], e.dxf.layer, M, Ramps[i], (i + 1) * 10000 + j * 100)
                else:
                    b = Beam(pts[1], pts[0], e.dxf.layer, Ramps[i], Ramps[i], (i + 1) * 10000 + j * 100)
            else:
                b = Beam(pts[1], pts[0], e.dxf.layer, Ramps[i], Ramps[i], (i + 1) * 10000 + j * 100)
            j += 1
            Beams.append(b)
    with open("./res/互通区匝道.mct", 'w+') as fid:
        fmct = open("./Data/template.mct", 'r')
        lines = fmct.readlines()
        fmct.close()
        nlist = []
        elist = []
        hdr = []
        for line in lines:
            fid.write(line)
        for b in Beams:
            b.make_nodes()
            # b.make_nodes_no_use()
            nlist += b.nlist
            elist += b.elist
            hdr += b.hdr
        fid.write("*NODE\n")
        for n in nlist:
            fid.write("%i,%.6f,%.6f,%.6f\n" % (n[0], n[1], n[2], n[3]))
        fid.write("*Element\n")
        for e in elist:
            fid.write(" %i,BEAM,%i,%i,%i,%i,0,0\n" % (e[0], e[1], e[2], e[3], e[4]))
        fid.write("*NODE\n")
        for n in hdr:
            fid.write("%i,%.6f,%.6f,%.6f\n" % (n[0], n[1], n[2], n[3]))
        fid.write("*NL-LINK\n")
        nl = 1
        for n in hdr:
            fid.write(" %i, %i, %i, HDR720, , 0, 0, \n" % (nl, n[0], n[4]))
            nl += 1
        fid.write("*CONSTRAINT\n")
        for n in hdr:
            fid.write("%i, 111111,\n" % (n[0]))
