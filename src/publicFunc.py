from scipy import interpolate
import numpy as np
import pylab as pl


def whats_mid(y0, y1, x0, x1, xi):
    k = (y1 - y0) / (x1 - x0)
    dx = xi - x0
    dy = dx * k
    return y0 + dy


class TendonInter(object):
    def __init__(self, xs, ys):
        self.Xlist = xs
        self.Ylist = ys
        self.func = interpolate.interp1d(self.Xlist, self.Ylist, kind='quadratic')

    def ShapeFunc(self):
        return self.func

    def plot(self, xmax):
        xnew = np.linspace(0, xmax, 101)
        ynew = self.func(xnew)
        pl.plot(xnew, ynew)
        pl.show()


def func_tendon(z0, z1, length, length_0):
    """
    抛物线-直线-抛物线型竖弯
    :param z0: 起点高
    :param z1: 平直段高
    :param length: 总投影长
    :param length_0: 平直段投影长
    :return:
    """
    dz = z1 - z0
    l = 0.5 * (length - length_0)
    AA = dz / l ** 2
    return lambda x: z0 if x < 0.5 * length_0 else z0 + AA * (x - 0.5 * length_0) ** 2



