import numpy as np
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


if __name__ == '__main__':
    T1z = interp1d([-16.5, -2, 0, 2, 16.5], [1.75, 0.315, 0.315, 0.315, 1.75], 'quadratic')
    T2z = interp1d([-16.5, -2, 0, 2, 16.5], [1.35, 0.125, 0.125, 0.125, 1.35], 'quadratic')
    T3z = interp1d([-16.5, -2, 0, 2, 16.5], [0.95, 0.125, 0.125, 0.125, 0.95], 'quadratic')
    T4z = interp1d([-16.5, -2, 0, 2, 16.5], [0.55, 0.125, 0.125, 0.125, 0.55], 'quadratic')
    T3y = interp1d([-16.5, -10, -4, 0, 4, 10, 16.5], [0, 0, +0.15, +0.15, +0.15, 0, 0], 'linear')
    T4y = interp1d([-16.5, -10, -4, 0, 4, 10, 16.5], [0, 0, -0.15, -0.15, -0.15, 0, 0], 'linear')

    xx = np.linspace(-16.5, 16.5, 67)
    yy1A = [0 * x + 1.55 for x in xx]
    yy3A = [T3y(x) + 1.55 for x in xx]
    yy4A = [T4y(x) + 1.55 for x in xx]
    yy1B = [0 * x - 1.55 for x in xx]
    yy3B = [T3y(x) - 1.55 for x in xx]
    yy4B = [T4y(x) - 1.55 for x in xx]
    zz1 = [T1z(x) for x in xx]
    zz2 = [T2z(x) for x in xx]
    zz3 = [T3z(x) for x in xx]
    zz4 = [T4z(x) for x in xx]

    for i in range(len(xx)):
        x0 = xx[i]
        y0 = zz1[i]
        print("%.3f,%.3f" % (x0 * 1e3, y0 * 1e3))

#    txt = "*TDN-PROFILE\n"
#    all_ele = "2000to2037"
#    txt += post_tendon(all_ele, xx, yy1A, zz1, "T1A", no=12)
#    txt += post_tendon(all_ele, xx, yy1A, zz2, "T2A", no=12)
#    txt += post_tendon(all_ele, xx, yy3A, zz3, "T3A", no=12)
#    txt += post_tendon(all_ele, xx, yy4A, zz4, "T4A", no=12)
#    all_ele = "1000to1037"
#    txt += post_tendon(all_ele, xx, yy1B, zz1, "T1B")
#    txt += post_tendon(all_ele, xx, yy1B, zz2, "T2B")
#    txt += post_tendon(all_ele, xx, yy3B, zz3, "T3B")
#    txt += post_tendon(all_ele, xx, yy4B, zz4, "T4B")
#    with open("TDN-33.mct", 'w+', encoding='GBK') as fid:
#        fid.write("*UNIT\n")
#        fid.write("   kN, M, KJ, C\n")
#        fid.write(txt)
#    #  print(txt)1000to1037 2000to2037
