from typing import List
import numpy as np
import pandas as pd
from ezdxf.math import Vec2, UCS, Vec3
from scipy.interpolate import interp1d


def post_tendon(ele, xlist, ylist, zlist, label, no=12):
    ret = ""
    name = label
    ret += "   NAME=%s, P%i, %s, 0, 0, SPLINE, 2D\n" % (name, no, ele)
    ret += "      后张束, USER, 0, 0, NO, \n"
    ret += "      STRAIGHT, 0, 0, 0, X, 0, 0\n"
    ret += "      0, YES, Y, 0\n"
    #    ret += "      Y=%i, 0, NO, 0, 0, NONE, , , , \n" % xlist[0]
    #    ret += "      Y=%i, 0, NO, 0, 0, NONE, , , , \n" % xlist[-1]
    for i, x in enumerate(xlist):
        y = ylist[i]
        ret += "      Y=%.3f, %.3f, NO, 0, 0, NONE, , , , \n" % (x, y)
    for i, x in enumerate(xlist):
        z = zlist[i]
        ret += "      Z=%.3f, %.3f, NO, 0, 0, NONE, , , , \n" % (x, z)
    return ret


def trans(seri, wcs):
    return [wcs.to_wcs(a) for a in seri]


def beam_aa_tendon(st, ed, post_type):
    l = st.distance(ed)
    ux = (ed - st).normalize()
    uy = ux.rotate_deg(90.0)
    uz = ux.cross(uy)
    xx = np.linspace(st.x, ed.x, 21)
    if post_type == 'aa':
        T1z = interp1d([st.x, (st + 13 * ux).x, (ed - 14 * ux).x, (ed - 2.5 * ux).x, ed.x], [1.75, 0.68, 0.68, 1.90, 1.90], 'quadratic')
        T2z = interp1d([st.x, (st + 13 * ux).x, (ed - 14 * ux).x, (ed - 2.5 * ux).x, ed.x], [1.35, 0.56, 0.56, 1.78, 1.78], 'quadratic')
        T3z = interp1d([st.x, (st + 13 * ux).x, (ed - 14 * ux).x, (ed - 2.5 * ux).x, ed.x], [0.95, 0.44, 0.44, 1.46, 1.46], 'quadratic')
        T4z = interp1d([st.x, (st + 13 * ux).x, (ed - 14 * ux).x, (ed - 2.5 * ux).x, ed.x], [0.55, 0.32, 0.32, 1.34, 1.34], 'quadratic')
    elif post_type == 'mm':
        T1z = interp1d([st.x, (st + 2.5 * ux).x, (st + 13.5 * ux).x, (ed - 13.5 * ux).x, (ed - 2.5 * ux).x, ed.x], [1.90, 1.90, 0.68, 0.68, 1.90, 1.90],
                       'quadratic')
        T2z = interp1d([st.x, (st + 2.5 * ux).x, (st + 13.5 * ux).x, (ed - 13.5 * ux).x, (ed - 2.5 * ux).x, ed.x], [1.78, 1.78, 0.56, 0.56, 1.78, 1.78],
                       'quadratic')
        T3z = interp1d([st.x, (st + 2.5 * ux).x, (st + 13.5 * ux).x, (ed - 13.5 * ux).x, (ed - 2.5 * ux).x, ed.x], [1.46, 1.46, 0.44, 0.44, 1.46, 1.46],
                       'quadratic')
        T4z = interp1d([st.x, (st + 2.5 * ux).x, (st + 13.5 * ux).x, (ed - 13.5 * ux).x, (ed - 2.5 * ux).x, ed.x], [1.34, 1.34, 0.32, 0.32, 1.34, 1.34],
                       'quadratic')
    elif post_type == 'dd':
        T1z = interp1d([st.x, (st + 2.5 * ux).x, (ed + 14 * ux).x, (ed - 13 * ux).x, ed.x], [1.90, 1.90, 0.68, 0.68, 1.75], 'quadratic')
        T2z = interp1d([st.x, (st + 2.5 * ux).x, (ed + 14 * ux).x, (ed - 13 * ux).x, ed.x], [1.78, 1.78, 0.56, 0.56, 1.35], 'quadratic')
        T3z = interp1d([st.x, (st + 2.5 * ux).x, (ed + 14 * ux).x, (ed - 13 * ux).x, ed.x], [1.46, 1.46, 0.44, 0.44, 0.95], 'quadratic')
        T4z = interp1d([st.x, (st + 2.5 * ux).x, (ed + 14 * ux).x, (ed - 13 * ux).x, ed.x], [1.34, 1.34, 0.32, 0.32, 0.55], 'quadratic')
    else:
        L1 = 18 if l > 35 else 14.5
        T1z = interp1d([st.x, (st + L1 * ux).x, (ed - L1 * ux).x, ed.x], [1.750, 0.575, 0.575, 1.750], 'quadratic')
        T2z = interp1d([st.x, (st + L1 * ux).x, (ed - L1 * ux).x, ed.x], [1.350, 0.425, 0.425, 1.350], 'quadratic')
        T3z = interp1d([st.x, (st + L1 * ux).x, (ed - L1 * ux).x, ed.x], [0.950, 0.275, 0.275, 0.950], 'quadratic')
        T4z = interp1d([st.x, (st + L1 * ux).x, (ed - L1 * ux).x, ed.x], [0.550, 0.125, 0.125, 0.550], 'quadratic')

    T1y = interp1d([st.x, ed.x], [st.y, ed.y], kind='linear')
    T2y = interp1d([st.x, ed.x], [st.y, ed.y], kind='linear')
    T3y = interp1d([st.x, ed.x], [st.y, ed.y], kind='linear')
    T4y = interp1d([st.x, ed.x], [st.y, ed.y], kind='linear')
    T1z0 = interp1d([st.x, ed.x], [st.z, ed.z], kind='linear')
    T2z0 = interp1d([st.x, ed.x], [st.z, ed.z], kind='linear')
    T3z0 = interp1d([st.x, ed.x], [st.z, ed.z], kind='linear')
    T4z0 = interp1d([st.x, ed.x], [st.z, ed.z], kind='linear')
    yy1 = [T1y(x) for x in xx]
    yy2 = [T2y(x) for x in xx]
    yy3 = [T3y(x) for x in xx]
    yy4 = [T4y(x) for x in xx]
    zz1 = [T1z0(x) + T1z(x) for x in xx]
    zz2 = [T2z0(x) + T2z(x) for x in xx]
    zz3 = [T3z0(x) + T3z(x) for x in xx]
    zz4 = [T4z0(x) + T4z(x) for x in xx]
    s1 = list(zip(xx, yy1, zz1))
    s2 = list(zip(xx, yy2, zz2))
    s3 = list(zip(xx, yy3, zz3))
    s4 = list(zip(xx, yy4, zz4))
    if post_type == 'aa' or post_type == 'ss':
        pts1 = [Vec3(a[0], a[1], float(a[2])) for a in s1]
        pts2 = [Vec3(a[0], a[1], float(a[2])) for a in s2]
        pts3 = [Vec3(a[0], a[1], float(a[2])) for a in s3]
        pts4 = [Vec3(a[0], a[1], float(a[2])) for a in s4]
    else:
        pts1 = [Vec3(a[0], a[1], float(a[2])) for a in s1][1:]
        pts2 = [Vec3(a[0], a[1], float(a[2])) for a in s2][1:]
        pts3 = [Vec3(a[0], a[1], float(a[2])) for a in s3][1:]
        pts4 = [Vec3(a[0], a[1], float(a[2])) for a in s4][1:]
    return [pts1, pts2, pts3, pts4]


def make_tendon(beam_name, elelist, pt_list: List['Vec3'], nos, isSS=False):
    txt = "*TDN-PROFILE\n"
    all_ele = elelist
    ptsT1 = []
    ptsT2 = []
    ptsT3 = []
    ptsT4 = []

    for ii in range(len(pt_list) - 1):
        if isSS:
            p1, p2, p3, p4 = beam_aa_tendon(pt_list[ii], pt_list[ii + 1], 'ss')
        else:
            if ii == 0:
                p1, p2, p3, p4 = beam_aa_tendon(pt_list[ii], pt_list[ii + 1], 'aa')
            elif ii == len(pt_list) - 2:
                p1, p2, p3, p4 = beam_aa_tendon(pt_list[ii], pt_list[ii + 1], 'dd')
            else:
                p1, p2, p3, p4 = beam_aa_tendon(pt_list[ii], pt_list[ii + 1], 'mm')
        ptsT1 += p1
        ptsT2 += p2
        ptsT3 += p3
        ptsT4 += p4

    pt_list = [ptsT1, ptsT2, ptsT3, ptsT4]
    for n in range(4):
        pt = pt_list[n]
        xss = [p.x for p in pt]
        yss = [p.y for p in pt]
        zss = [p.z for p in pt]
        txt += post_tendon(all_ele, xss, yss, zss, "POST%sT%i" % (beam_name, n + 1), no=nos[n])
    return txt


if __name__ == '__main__':
    locs = pd.read_excel(".\SS\SS模型参数.xlsx", sheet_name="坐标", header=None, index_col=0)
    data = pd.read_excel('.\SS\SS模型参数.xlsx', sheet_name='后张')
    with open('.\SS\SS后张束.mct', 'w+', encoding='GBK') as fid:
        fid.write("*UNIT\n")
        fid.write("   kN, M, KJ, C\n")
        for i, row in data.iterrows():
            nlist = row[3:].values.tolist()
            coords = [Vec3(locs.at[ni, 1] * 1e-3, locs.at[ni, 2] * 1e-3, locs.at[ni, 3] * 1e-3) for ni in nlist]
            int_list = list(map(int, row['Nos'].split(',')))
            txt = make_tendon(row['Beam'], row['Es'], coords, isSS=True, nos=int_list)
            fid.write(txt)
