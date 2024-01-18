from ezdxf.math import Vec2, Vec3, ConstructionLine
from srbpy import Align

connect = [
    ['B11', 101, 102],
    ['S12', 103, ],
    ['S12', 104, ],
    ['S12', 105, ],
    ['S12', 106, ],
    ['B13', 309, 308, 307, 109, 108, 107],


    ['B14', 310, 111, 110],
    ['B14', 503, 502, 501],
    ['B14', 506, 505, 504],

    ['B21', 201, 202],
    ['S22', 203, ],
    ['S22', 204, ],
    ['S22', 205, ],
    ['S22', 206, ],
    ['S22', 207, ],
    ['B23', 209, 208],
    ['B23', 211, 210],
    ['B23', 213, 212],
    ['B23', 215, 214],

    ['B31', 306, 305],
    ['S32', 301, ],
    ['S32', 302, ],
    ['S32', 303, ],
    ['S32', 304, ],

    ['S41', 403, ],
    ['S41', 401, ],
    ['S41', 402, ],
    ['S41', 404, ],
    ['B42', 406, 405],
    ['B42', 408, 407],
    ['B42', 410, 409],

    ['B51', 510, 509, 508, 507],
    ['B51', 514, 513, 512, 511],
    ['B51', 518, 517, 516, 515],

    ['B52', 413, 412, 411, 217, 216],
    ['B52', 416, 415, 414, 219, 218],
    ['B52', 419, 418, 417, 221, 220],




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
        self.beam_id = int(self.n0 / 100)
        loc, blist, trans_loc = self.get_location(int(self.n0 / 100))
        self.bridge = blist[0]

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
