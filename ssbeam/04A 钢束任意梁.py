from typing import List
import numpy as np
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


def make_tendon(elelist, st_list: List['Vec2'], ed_list: List['Vec2'], out_file):
    lab = 'ABCDEFG'
    txt = "*TDN-PROFILE\n"
    for i in range(len(st_list)):
        st = st_list[i]
        ed = ed_list[i]
        all_ele = elelist[i]
        l = st.distance(ed)
        ux = (ed - st).normalize().vec3
        uy = ux.rotate_deg(90.0)
        uz = Vec3(0, 0, 1)
        ori = (st + 0.5 * l * ux).vec3
        wcs = UCS(ori, ux, uy, uz)
        T1z = interp1d([-0.5 * l, -0.5 * l + 18, 0, 0.5 * l - 18, 0.5 * l], [1.75, 0.275, 0.275, 0.275, 1.75], 'quadratic')
        T2z = interp1d([-0.5 * l, -0.5 * l + 18, 0, 0.5 * l - 18, 0.5 * l], [1.35, 0.125, 0.125, 0.125, 1.35], 'quadratic')
        T3z = interp1d([-0.5 * l, -0.5 * l + 18, 0, 0.5 * l - 18, 0.5 * l], [0.95, 0.125, 0.125, 0.125, 0.95], 'quadratic')
        T4z = interp1d([-0.5 * l, -0.5 * l + 18, 0, 0.5 * l - 18, 0.5 * l], [0.55, 0.125, 0.125, 0.125, 0.55], 'quadratic')
        T3y = interp1d([-0.5 * l, -0.5 * l + 10, - 0.5 * l + 16, 0, 0.5 * l - 16, 0.5 * l - 10, 0.5 * l], [0, 0, +0.15, +0.15, +0.15, 0, 0], 'linear')
        T4y = interp1d([-0.5 * l, -0.5 * l + 10, - 0.5 * l + 16, 0, 0.5 * l - 16, 0.5 * l - 10, 0.5 * l], [0, 0, -0.15, -0.15, -0.15, 0, 0], 'linear')
        xx = np.linspace(-0.5 * l, 0.5 * l, 81)
        yy1 = [0 * x for x in xx]
        yy2 = [0 * x for x in xx]
        yy3 = [T3y(x) for x in xx]
        yy4 = [T4y(x) for x in xx]
        zz1 = [T1z(x) for x in xx]
        zz2 = [T2z(x) for x in xx]
        zz3 = [T3z(x) for x in xx]
        zz4 = [T4z(x) for x in xx]
        s1 = list(zip(xx, yy1, zz1))
        s2 = list(zip(xx, yy2, zz2))
        s3 = list(zip(xx, yy3, zz3))
        s4 = list(zip(xx, yy4, zz4))
        pts1 = trans([Vec3(a[0], a[1], float(a[2])) for a in s1], wcs)
        pts2 = trans([Vec3(a[0], a[1], float(a[2])) for a in s2], wcs)
        pts3 = trans([Vec3(a[0], a[1], float(a[2])) for a in s3], wcs)
        pts4 = trans([Vec3(a[0], a[1], float(a[2])) for a in s4], wcs)
        pt_list = [pts1, pts2, pts3, pts4]
        for n in range(4):
            pt = pt_list[n]
            xss = [p.x for p in pt]
            yss = [p.y for p in pt]
            zss = [p.z for p in pt]
            txt += post_tendon(all_ele, xss, yss, zss, "T%i%s" % (n + 1, lab[i]), no=15)
        # txt += post_tendon(all_ele, pts2, yy1A, zz2, "T2%s" % (lab[i]), no=16)
        # txt += post_tendon(all_ele, pts3, yy3A, zz3, "T3%s" % (lab[i]), no=16)
        # txt += post_tendon(all_ele, pts4, yy4A, zz4, "T4%s" % (lab[i]), no=16)
    with open(out_file, 'w+', encoding='GBK') as fid:
        fid.write("*UNIT\n")
        fid.write("   kN, M, KJ, C\n")
        fid.write(txt)


if __name__ == '__main__':
    ale = ["1000to1043",
           "2000to2043",
           "3000to3043",
           "4000to4043",
           "5000to5042",
           "6000to6041", ]
    stpts = [
        Vec2(-20, 1.55),
        Vec2(-20, -0.09),
        Vec2(-20.051342, -1.7291961),
        Vec2(-20.153833, -3.3659905),
        Vec2(-20.305606, -4.9989525),
        Vec2(-20.507403, -6.6264898),
    ]
    edpts = [
        Vec2(20.18, 1.55),
        Vec2(20.180296, -1.3485049),
        Vec2(20.07008, -4.2414709),
        Vec2(19.425583, -7.0446293),
        Vec2(18.398026, -9.7977947),
        Vec2(17.03579, -12.500898),
    ]

    make_tendon(ale, stpts, edpts, 'R15R16.mct')
