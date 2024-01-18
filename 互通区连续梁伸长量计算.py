from typing import List
from typing import List

import ezdxf
import matplotlib.pyplot as plt
import pandas as pd
from ezdxf.math import ConstructionArc as cArc, Vec2
from ezdxf.math import ConstructionLine as cLine
from ezdxf.math import ConstructionPolyline as cPline
from ezdxf.entities.line import Line as dLine
import numpy as np
from operator import itemgetter, attrgetter
from scipy.interpolate import interp1d
from itertools import chain


def get_z(tendons, xi, tol=0.002):
    ret = []
    cutLine = cLine(Vec2(xi, -100), Vec2(xi, 100))
    for e in tendons:
        if isinstance(e, cLine):
            x = cutLine.intersect(e)
        else:
            x = e.intersect_line(cutLine)
        if x is None:
            continue
        elif len(x) == 0:
            continue
        else:
            ret.append(x)
    if len(ret) == 0:
        raise ValueError(xi)
    elif len(ret) == 1:
        try:
            return ret[0].y
        except AttributeError:
            return ret[0][0].y
    else:
        try:
            ys = [a.y for a in ret]
        except AttributeError:
            return None
        assert abs(max(ys) - min(ys)) <= tol
        return np.mean(ys)


def cmp(a, b):
    return (a > b) - (a < b)


def cmp_arc_line(x):
    if isinstance(x, cLine):
        a = 0.5 * (x.start.x + x.end.x)
    else:
        a = 0.5 * (x.start_point.x + x.end_point.x)
    return a


def dxf2pl(dxf_file, layer_name, size=0.2):
    lines = dxf_file.modelspace().query('Solid line[layer=="%s"]' % layer_name)
    arcs = dxf_file.modelspace().query('ARC[layer=="%s"]' % layer_name)
    data = []
    for l in lines:
        data.append(cLine(l.dxf.start, l.dxf.end))
    for a in arcs:
        data.append(cArc(a.dxf.center, a.dxf.radius, a.dxf.start_angle, a.dxf.end_angle))
    Tendon = sorted(data, key=lambda x: cmp_arc_line(x))
    if isinstance(Tendon[0], cLine):
        st_x = min(Tendon[0].start.x, Tendon[0].end.x)
    else:
        st_x = min(Tendon[0].start_point.x, Tendon[0].end_point.x)
    if isinstance(Tendon[-1], cLine):
        ed_x = max(Tendon[-1].start.x, Tendon[-1].end.x)
    else:
        ed_x = max(Tendon[-1].start_point.x, Tendon[-1].end_point.x)
    ret = []
    for xx in np.linspace(st_x, ed_x, int(np.round((ed_x - st_x) / size, 0))):
        r = get_z(Tendon, xx)
        assert r is not None
        try:
            ret.append([xx, r])
        except TypeError:
            raise TypeError(xx)
    return ret


def get_theLength(data):
    Sum = 0
    pts = [Vec2(a[0], a[1]) for a in data]
    for i, p in enumerate(pts):
        if i != 0:
            Sum += cLine(pts[i - 1], pts[i]).length()
    return Sum


def get_allLength(data, strandsNo, isOneSide):
    """
    获取钢束长度
    :param data:
    :param strandsNo:
    :param isOneSide:
    :return: 理论长度，导管长度，下料长度
    """
    tLength = get_theLength(data)

    if strandsNo <= 18:
        AAnchorReserve = 0.75
    elif strandsNo <= 22:
        AAnchorReserve = 0.75
    elif strandsNo <= 27:
        AAnchorReserve = 0.80
    else:
        AAnchorReserve = 0.80

    if strandsNo <= 17:
        AAnchorB = 0.325
    elif strandsNo <= 22:
        AAnchorB = 0.325
    elif strandsNo <= 27:
        AAnchorB = 0.43
    else:
        AAnchorB = 0.43

    if strandsNo <= 17:
        AAnchorF = 0.075
    elif strandsNo <= 19:
        AAnchorF = 0.075
    elif strandsNo <= 22:
        AAnchorF = 0.08
    elif strandsNo <= 24:
        AAnchorF = 0.082
    elif strandsNo <= 27:
        AAnchorF = 0.085
    else:
        AAnchorF = 0.085

    if strandsNo <= 17:
        PAnchorB = 0.72
    elif strandsNo <= 19:
        PAnchorB = 0.72
    elif strandsNo <= 22:
        PAnchorB = 0.90
    elif strandsNo <= 27:
        PAnchorB = 1.0
    else:
        raise NotImplementedError
    tLength = np.round(tLength, 4)
    if isOneSide:
        DuctLength = np.round(tLength - AAnchorB - 0.02 - PAnchorB, 4)
        Length = np.round(0.2 + AAnchorReserve + 0.020 + AAnchorF * 3 + tLength + 0.2, 4)
    else:
        DuctLength = np.round(tLength - 2 * (AAnchorB + 0.02), 4)
        Length = np.round(2 * (0.2 + AAnchorReserve + 0.020 + AAnchorF * 3) + tLength, 4)
    return tLength, DuctLength, Length


# def get_friction(data)

def one_way_loss(pts, fcon, K, mu):
    f0 = fcon
    ret = []
    for i, pt in enumerate(pts):
        if i == 0:
            f0 = f0
        elif i == len(pts) - 1:
            xi = pt.distance(pts[i - 1])
            dfps2 = f0 * (1 - np.exp(-(K * xi)))
            f0 = f0 - abs(dfps2)
        else:
            l0 = cLine(pts[i - 1], pt)
            l1 = cLine(pt, pts[i + 1])
            dA = abs(l1.ray.angle - l0.ray.angle)
            xi = pt.distance(pts[i - 1])
            dfps1 = f0 * (1 - np.exp(-(mu * dA + K * xi)))
            f0 = f0 - abs(dfps1)
        ret.append(Vec2(pt.x, f0))
    return ret


def get_fs_pl(tendon: 'cPline', fcon, K, mu, isOneSide) -> 'cPline':
    pts = tendon._vertices
    ll = pts[-1].x
    pts_rev = [Vec2(ll - a.x, a.y) for a in pts]
    pts_rev.sort()
    fs0 = one_way_loss(pts, fcon, K, mu)
    if isOneSide:
        return cPline(fs0)
    else:
        fs1 = one_way_loss(pts_rev, fcon, K, mu)
        fs2 = [Vec2(ll - a.x, a.y) for a in fs1]
        fs2.sort()
        ret = []
        for ii, v2 in enumerate(fs0):
            f0 = v2.y
            f1 = fs2[ii].y
            x0 = v2.x
            ret.append(Vec2(x0, max(f0, f1)))
        return cPline(ret)


def get_elongation(data, nstrand, isOneSide, ft=1.0):
    if isOneSide:
        xd, yd = my_diff(data[:, 0], data[:, 1])
    else:
        xd, yd = my_diff(data[0:int(len(data) / 2), 0], data[0:int(len(data) / 2), 1])
    rad = np.arctan(yd)  # 角度
    x0, fs = get_fs(1395, xd, rad)
    tlen, dlen, wlen = get_allLength(data, nstrand, isOneSide)
    elong = fs / 197000 * np.diff(xd)
    return "%.3f" % (np.sum(elong) * ft)


def my_int(xx, yy):
    sum_y = []
    sum_x = []
    ret_y = []
    for i in range(len(xx) - 1):
        yi = (yy[i + 1] + yy[i]) * 0.5
        sum_y.append(yi)
        sum_x.append((xx[i + 1] + xx[i]) * 0.5)
    for i in range(len(sum_y)):
        ret_y.append(np.sum(sum_y[0:i]))
    return np.array(sum_x), np.array(ret_y)


def my_diff(xx, yy):
    xout = (xx[0:-1] + xx[1:]) * 0.5
    yout = np.diff(yy) / (xx[1:] - xx[0:-1])
    assert len(xout) == len(yout)
    return xout, yout


def my_sum(arr):
    ret = []
    for i in range(len(arr)):
        ret.append(np.sum(arr[0:i]))
    return np.array(ret)


def get_rad_int(xi, angle):
    rad_d = np.diff(angle)  # 角度差分
    rad_d_abs = np.abs(rad_d)  # 角度差分绝对值
    xdd, ydd = my_diff(xi, angle)
    rad_int_abs = my_sum(rad_d_abs)  # 差分求和
    rad_int_abs_re = rad_int_abs[-1] - rad_int_abs  # 求逆
    return xdd, rad_int_abs, rad_int_abs_re


def fpj(fcon, xi, rad, K=0.0015, mu=0.25):
    return fcon * (1 - np.exp(-(mu * rad + K * xi)))


def get_fs(fcon, xi, angle):
    x2d, rad_from_st, rad_from_ed = get_rad_int(xi, angle)
    fs0 = fpj(fcon, x2d, rad_from_st)
    fs1 = fpj(fcon, (x2d[-1] - x2d)[::-1], rad_from_ed[::-1])[::-1]
    aa = np.array([fs0, fs1]).T
    fs = np.array([min(a) for a in aa])
    return x2d, fcon - fs


def get_cline(LL: 'dLine'):
    p0 = LL.dxf.start.vec2
    p1 = LL.dxf.end.vec2
    xx = 0.5 * (p0.x + p1.x)
    yy = 0.5 * (p0.y + p1.y)
    return [xx, yy]


def get_pts(LL: 'dLine'):
    p0 = LL.dxf.start.vec2
    p1 = LL.dxf.end.vec2
    return [p0, p1]


def get_vertical_val(spans, x0, zval):
    xs = []
    z1, z2, z3 = zval
    zs = [z1]
    for i, sp in enumerate(spans):
        if i == 0:
            xs += [13000, sp - 27000, 11500, 2500]
            zs += [z2, z2, z3, z3]
        elif i == len(spans) - 1:
            xs += [2500, 11500, sp - 27000, 13000]
            zs += [z3, z2, z2, z1]
        else:
            xs += [2500, 11000, sp - 27000, 11000, 2500]
            zs += [z3, z2, z2, z3, z3]
    new_x = [x0]
    for j in xs:
        new_x.append(new_x[-1] + j)
    return new_x, zs


if __name__ == "__main__":
    data = pd.read_excel("./Data/互通区梁段信息.xlsx")
    for gr, gpd in data.groupby("BR"):
        pts = []
        Ls = []
        for i, row in gpd.iterrows():
            pts.append(Vec2(row['X'], row['Y']))
            if float(row['ST']) != 1:
                Ls.append(pts[-1].distance(pts[-2]))
        Ls = np.array(Ls) * 1000
        xx1, zz1 = get_vertical_val(Ls, 0, [1750, 680, 1900])
        xx2, zz2 = get_vertical_val(Ls, 0, [1350, 560, 1780])
        xx3, zz3 = get_vertical_val(Ls, 0, [950, 440, 440])
        xx4, zz4 = get_vertical_val(Ls, 0, [550, 320, 320])
        Tendons = [zip(xx1, zz1), zip(xx2, zz2), zip(xx3, zz3), zip(xx4, zz4), ]
        for Td in Tendons:
            tds = [list(np.array(a) * 1e-3) for a in Td]  # f = 1
            if "W" in gr:
                NoS = 10
            else:
                NoS = 12
            TheL, DuctL, WorkL = get_allLength(tds, NoS, True)
            fs = get_fs_pl(cPline([Vec2(a) for a in tds]), 1395 - 15, 0.0015, 0.23, True)
            dataX = [p.x for p in fs]
            dataY = [p.y for p in fs]
            f = interp1d(dataX, dataY)
            L = tds[-1][0]
            num_seg = int(L / 0.01)
            d_seg = L / num_seg
            xs = np.linspace(d_seg * 0.5, L - d_seg * 0.5, num_seg)
            flist = np.array([f(x) - 7.0 for x in xs])
            Es = 197e3
            d_list = flist / Es * d_seg
            elong = sum(d_list)
            print("%4s: %8.3f , %8.3f , %8.3f" % (gr, WorkL, DuctL, elong))
            # print("%s,"%(TheL, DuctL, WorkL))

#     doc = ezdxf.readfile(r"./doc/SNG-EX3-05钢束.dxf")
#     for Beam in ['05', '06', '07']:
#         ns = [22, ] * 4
#         fts = [1.1, ] * 7
#         for i, strands in enumerate(ns):
#             name = '%sT%i' % (Beam, i + 1)
#             tds = dxf2pl(doc, name)
#             # Length = get_theLength(tds)
#             TheL, DuctL, WorkL = get_allLength(tds, ns[i], True)
#             fs = get_fs_pl(cPline([Vec2(a) for a in tds]), 1395, 0.0015, 0.25, True)
#             dataX = [p.x for p in fs]
#             dataY = [p.y for p in fs]
#             f = interp1d(dataX, dataY)
#             L = tds[-1][0]
#             num_seg = int(L / 0.01)
#             d_seg = L / num_seg
#             xs = np.linspace(d_seg * 0.5, L - d_seg * 0.5, num_seg)
#             flist = np.array([f(x) - 7.0 for x in xs])
#             Es = 197e3
#             d_list = flist / Es * d_seg
#             elong = sum(d_list)
#             print("%4s: %8.3f , %8.3f , %8.3f" % (name, WorkL, DuctL, elong))
#
