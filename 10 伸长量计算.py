from typing import List

import ezdxf
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


def dxf2pl(filename, st_x, ed_x, size=0.2):
    with open(filename, 'r', encoding='utf-8') as fid:
        data = fid.readlines()
    ret = []
    Tendon = []
    for i, txt in enumerate(data):
        if txt.__contains__("直线"):
            Tendon.append(make_line(data, i))
        if txt.__contains__("圆弧"):
            Tendon.append(make_arc(data, i))
    for xx in np.linspace(st_x, ed_x, int(np.round((ed_x - st_x) / size, 0))):
        r = get_z(Tendon, xx)
        try:
            ret.append([xx, r])
        except TypeError:
            raise TypeError(xx)
    ret = np.array(ret)
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


if __name__ == "__main__":
    doc = ezdxf.readfile(r".\Data\竖弯大样.dxf")
    pl = doc.modelspace().query('LWPOLYLINE[layer=="%s"]' % 'BT4').first
    fs = get_fs_pl(cPline(pl.vertices()), 1860 * 0.80, 0.0015, 0.23, True)
    dataX = [p.x for p in fs]
    dataY = [p.y for p in fs]
    f = interp1d(dataX, dataY)
    print(f(0.5) - 7)
    print(f(0.5 * 45) - 7)
    print(f(40) - 7)
    print(f(45) - 7)
    print(f(3.5 * 45.0) - 7)
    print(f(4 * 45.0) - 7)
    # print(f(2.5 * 45))
    # print(f(3.5 * 45))
    # print(fs.vertex_at(44.5))
#     for i in range(226):
#         vv = fs.vertex_at(i)
#         print("%.1f,%.1f" % (vv.x, vv.y))
#         f = 1
#     ns = [19, 19, 19, 17, ] * 3 + [12, ] * 6
#     fts = [1.1, ] * 4 + [1.05, ] * 4 + [1.0, ] * 4 + [1.0, ] * 6
#     TP = ['A', 'B', 'C']
#     side = [
#         False, True, False
#     ]
#     for i, t in enumerate(TP):
#         for j in range(4):
#             name = '%sT%i' % (t, j + 1)
#             pl = doc.modelspace().query('LWPOLYLINE[layer=="%s"]' % name).first
#             fs = get_fs_v2(cPline(pl.vertices()), 1860 * 0.75, 0.0015, 0.23, False)
#
#             f = 1
#             # newLines = sorted(lines, key=attrgetter("dxf.start.x"))
#             # pts = [get_pts(L) for L in newLines]
#             # pts = list(chain.from_iterable(pts))
#             # pts = list(set(pts))
#             # pts.sort()
#             # newClines = np.array([[a.x, a.y] for a in pts])
#             # print(" %s 伸长量: %s mm" % (name, get_elongation(newClines, 12, side[i])))
