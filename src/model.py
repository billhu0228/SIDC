from typing import List

import matplotlib.pyplot as plt
# from matplotlib.patches import Polygon
# from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pylab
import numpy as np
from .units import *
import math


class Concrete():
    def __init__(self):
        fc = 65.0

    def in_plot(x0, x1, y0, y1, inter):
        kk = (y1 - y0) / (x1 - x0)
        dx = inter - x0
        dy = kk * dx
        return y0 + dy

    def _conc_(eps: float, fcu, gamma_m):
        # y=ax**2;
        x1 = 2.44e-4 * np.sqrt(fcu / gamma_m)
        y1 = 0.67 * fcu / gamma_m
        a = y1 / x1 ** 2
        if eps <= x1:
            fake_y = a * (x1 - eps) ** 2
            return y1 - fake_y
        else:
            return y1


class TSection(object):
    def __init__(self, w, ws, h1, h):
        self.W = w
        self.W_top = ws
        self.H_bot = h1
        self.H = h
        self.Area = self.H_bot * self.W + self.W_top * (self.H - self.H_bot)


class Tendon(object):
    def __init__(self, name: str, strand: float, num_strand: int, shapeFunc, func_ft=1.0):
        self.Name = name
        self.StrandAs = strand
        self.NumStrands = num_strand
        self.GetYFunc = shapeFunc
        self.func_ft = func_ft

    def GetY(self, x0):
        return self.GetYFunc(x0 / self.func_ft) * self.func_ft

    def GetAs(self):
        return self.StrandAs * self.NumStrands


class Rebar(object):
    def __init__(self, name: str, rebarAs: float, num_rebar: int, Y: float):
        self.Name = name
        self.RebarAs = rebarAs
        self.NumRebars = num_rebar
        self.Y = Y

    def GetY(self, x0):
        return self.Y

    def GetAs(self):
        return self.RebarAs * self.NumRebars


class CrossBeam(object):
    def __init__(self, length: float, section: TSection, bRebar: Rebar, tRebar: Rebar):
        self.Length = length
        self.Section = section
        self.BotRebars = bRebar
        self.TopRebars = tRebar
        self.TendonList: List[Tendon] = []

    def AssignTendon(self, theTendon: Tendon):
        self.TendonList.append(theTendon)

    def width_func(self, x0):
        return self.Section.W if x0 < self.Section.H_bot else self.Section.W_top

    # def con_force_from_bot(self,xh: float, size: float = 1):
    #     x0 = self.Section.H - xh
    #     x1 = self.Section.H
    #     eps0 = 0
    #     eps1 = 0.003
    #     npts = int(xh / size)
    #     e_size = xh / npts
    #     NN = 0
    #     for ii in range(npts):
    #         z0 = x0 + ii * e_size + 0.5 * e_size
    #         width = self.width_func(z0)
    #         eps = in_plot(x0, x1, eps0, eps1, z0)
    #         sigma = _conc_(eps, fcu, gamma_m_c)
    #         NN += sigma * e_size * width
    #     return NN
    def GetMomentTensTop(self, x0, fps):
        Aps = 0
        YpsAps = 0
        for t in self.TendonList:
            Aps += t.GetAs()
            YpsAps += t.GetAs() * t.GetY(x0)
        dp = YpsAps / Aps

        As = self.TopRebars.GetAs()
        fs = 500.0
        ds = self.TopRebars.GetY(x0)
        Asc = self.BotRebars.GetAs()
        fsc = 250.0
        dsc = self.BotRebars.GetY(x0)
        fc = 45.0
        b = self.Section.W
        beta1 = max(0.85 - (fc - 28) / 7.0 * 0.05, 0.65)
        k = 2 * (1.04 - 1674 / 1860)
        c1 = Aps * 1860 + As * fs - Asc * fs * 0.5
        c2 = 0.85 * fc * beta1 * b + k * Aps * 1860 / dp
        c = c1 / c2
        assert c <= self.Section.H_bot
        a = c * beta1
        Mn = Aps * fps * (dp - 0.5 * a) + As * fs * (ds - 0.5 * a) - Asc * fs * 0.6 * (dsc - 0.5 * a)
        return Mn

    def GetMomentTensBot(self, x0, fps):
        Aps = 0
        YpsAps = 0
        for t in self.TendonList:
            Aps += t.GetAs()
            YpsAps += t.GetAs() * t.GetY(x0)
        dp = self.Section.H - (YpsAps / Aps)

        As = self.BotRebars.GetAs()
        fs = 500.0
        ds = self.Section.H - self.BotRebars.GetY(x0)
        Asc = self.TopRebars.GetAs()
        dsc = self.Section.H - self.TopRebars.GetY(x0)
        fc = 45.0

        b = self.Section.W_top
        beta1 = max(0.85 - (fc - 28) / 7.0 * 0.05, 0.65)
        k = 2 * (1.04 - 1674 / 1860)
        c1 = Aps * 1860 + As * fs - Asc * fs
        c2 = 0.85 * fc * beta1 * b + k * Aps * 1860 / dp
        c = c1 / c2
        a = c * beta1
        Mn = Aps * fps * (dp - 0.5 * a) + As * fs * (ds - 0.5 * a) - Asc * fs * 0.5 * (dsc - 0.5 * a)
        return Mn

    def GetVc(self, beta):
        # beta = 2.0
        fc = PSI(45.0) * 1e-3
        bv = INCH(self.Section.W_top)
        dv = INCH(self.Section.H - 100)
        vc_is = 0.0316 * beta * np.sqrt(fc) * bv * dv
        return NEWTON(vc_is * 1e3)

    def GetVs(self, s: float, num: int, dia: float, theta_deg: float):
        theta = math.radians(theta_deg)
        Av = num * (np.pi * 0.25 * INCH(dia) * INCH(dia))
        fy = PSI(500) * 1e-3  # ksi
        dv = INCH(self.Section.H - 100)
        cot = np.cos(theta) / np.sin(theta)
        s_inch = INCH(s)
        Vs = Av * fy * dv * cot / s_inch
        return NEWTON(Vs * 1000)

    def Get_eps_x(self, x0, dv, theta_rad: float, NMV: List[float]):
        Mu = NMV[1]
        Vu = NMV[2]
        Nu = NMV[0]
        p1 = np.abs(Mu) / dv
        p2 = 0.5 * Nu
        p3 = 0.5 * np.abs(Vu - self.GetVp(x0)) * np.cos(theta_rad) / np.sin(theta_rad)
        Aps = 0
        for t in self.TendonList:
            if t.GetY(x0) < 0.5 * self.Section.H:
                Aps += t.GetAs()
        p4 = 0.7 * 1860.0 * Aps
        As = self.BotRebars.GetAs()
        Asc = self.TopRebars.GetAs()

        Es = 200000.0
        Ep = MPA(28500 * 1000)

        fz = p1 + p2 + p3 - p4
        m1 = 2 * (Es * As + Ep * Aps)

        eps_x = fz / m1
        if eps_x > 0.001:
            eps_x = 0.001
        assert eps_x <= 0.001
        if eps_x < 0:
            Ec = 32199.0
            if self.Section.H_bot < self.Section.H * 0.5:
                Ac = self.Section.H * 0.5 * self.Section.W
            else:
                Ac = self.Section.Area - self.Section.H * 0.5 * self.Section.W_top
            m3 = 2 * (Es * As + Ec * Ac + Ep * Aps)
            eps_x = fz / m3
        return eps_x

    def GetVp(self, x0, stress=0.75 * 0.75 * 1860.0):
        f_all = 0
        for t in self.TendonList:
            z2 = t.GetY(x0 + 0.5)
            z1 = t.GetY(x0 - 0.5)
            ang = np.arctan(z2 - z1)
            a_deg = math.degrees(ang)
            f = t.GetAs() * stress * np.sin(ang)
            f_all += f
            # print("%s: %.1f° | Vpi=%.0f kN" % (t.Name, a_deg, f * 1e-3))
        return f_all

    def get_vu(self, x0, Vu, dv):
        fz = np.abs(Vu - 0.9 * self.GetVp(x0))
        fm = 0.9 * self.Section.W_top * dv
        return fz / fm

    def check_longitudinal_rebar(self, x0, dv, theta_rad: float, NMV: List[float], VS=0):
        Mu = NMV[1]
        Vu = NMV[2]
        Nu = NMV[0]
        p1 = np.abs(Mu) / dv / 0.9
        p2 = 0.5 * Nu / 0.9
        p3 = (np.abs(Vu / 0.9 - self.GetVp(x0)) - 0.5 * VS) * np.cos(theta_rad) / np.sin(theta_rad)
        Aps = 0
        for t in self.TendonList:
            if t.GetY(x0) < 0.5 * self.Section.H:
                Aps += t.GetAs()

        As = self.BotRebars.GetAs()

        return (Aps * 0.75 * 1860.0 + As * 500.0) > (p1 + p2 + p3)

    def PlotEvolopFigure(self, path):
        xnew = np.linspace(0, self.Length, 201)
        moment_bot = []
        moment_top = []
        for x in xnew:
            moment_bot.append(self.GetMomentTensBot(x, 1860 * 0.75 * 0.75))
            moment_top.append(self.GetMomentTensTop(x, 1860 * 0.75 * 0.75))
        moment_bot = np.array(moment_bot)
        moment_top = np.array(moment_top)
        inch = 25.4
        mm = 1.0 / 25.4
        width = 160
        heigh = 50
        margins = [15, 10, 2, 2]
        fig = plt.figure(figsize=(width * mm, heigh * mm))
        ax = fig.add_axes([margins[0] / width, margins[1] / heigh, 1 - (margins[0] + margins[2]) / width, 1 - (margins[1] + margins[3]) / heigh])
        ax.grid(True)
        cv = FigureCanvas(fig)
        ax.set_xlabel('Location (mm)')
        ax.set_ylabel('Moment ()')

        ax.plot(xnew * 0.001, moment_bot * 1e-6, color='r', label="Bot")
        ax.plot(xnew * 0.001, moment_top * -1e-6, color='b', label="Top")

        ax.legend(loc=1, ncol=1, shadow=True)
        cv.print_figure(path, dpi=300)
        pass


if __name__ == "__main__":
    def f1(x0):
        return 1.2 * x0


    N1 = Tendon("N1", 140, 22, f1)

    print(N1.GetY(30))
