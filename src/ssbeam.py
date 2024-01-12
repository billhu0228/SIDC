from ezdxf.math import Vec2, Vec3, ConstructionLine
from srbpy import Align

connect = [
    ['B1', 101],
    ['B1', 102],
]


class SSBeam:
    def __init__(self, st: Vec3, ed: Vec3,  nd_base: int):
        p0 = st
        p1 = ed
        self.line = (p0, p1)
        self.beam_type = 'SS'
        self.n0 = nd_base
        self.nlist = []
        self.elist = []
        self.hdr = []
        self.lnr = []
        self.beam_id = int(self.n0 / 100)
        #loc, blist, trans_loc = self.get_location(int(self.n0 / 100))
        # self.bridge = blist[0]

    def get_location(self, beam_id):
        for e in connect:
            if e.__contains__(beam_id):
                theB = e[0]
                part = [a for a in connect if a[0] == theB]
                return e.index(beam_id), e, part.index(e)
        return None

    def make_nodes(self):
        pts = self.get_pts()
        n0 = self.n0
        beam_id = int(n0 / 100)
        for pt in pts:
            pp = pt
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
