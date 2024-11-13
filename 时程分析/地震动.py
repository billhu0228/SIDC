import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylab
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.pyplot import MultipleLocator
from matplotlib import ticker

# -------------------------------------------------------------------------------
# 绘图参数设置
# -------------------------------------------------------------------------------
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
pylab.mpl.rcParams['axes.unicode_minus'] = False
pylab.mpl.rcParams['font.size'] = 10
pylab.mpl.rcParams['legend.fontsize'] = u'small'
pylab.mpl.rcParams['xtick.labelsize'] = u'small'
pylab.mpl.rcParams['ytick.labelsize'] = u'small'


def PrintSPD(Ts, S, file):
    with open(file, "w+") as fid:
        fid.write("*UNIT,GRAV\n")
        fid.write("*TYPE,ACCEL\n")
        fid.write("*Data\n")
        for i, t in enumerate(Ts):
            fid.write("%.4E,%.6f\n" % (t, S[i]))


def GetS(Smax, Tg, T):
    T0 = 0.1
    if T < T0:
        return Smax * (0.6 * T / T0 + 0.4)
    elif T < Tg:
        return Smax
    else:
        return Smax * (Tg / T)


def GetDES(Smax, Tg, Ta=0.0, Tb=10.0, Tstep=0.01):
    Tlist = np.linspace(Ta, Tb, int(np.round((Tb - Ta) / Tstep + 1)))
    Slist = [GetS(Smax, Tg, ti) for ti in Tlist]
    return [Tlist.tolist(), Slist]


def GetSmax(Ci, Cs, Cd, A):
    return 2.5 * Ci * Cs * Cd * A


def GetCd(xi):
    return max(1 + (0.05 - xi) / (0.08 + 1.6 * xi), 0.55)


if __name__ == "__main__":
    Cd0 = GetCd(0.05)
    print("Cd=%.4f" % Cd0)
    Smax_E1x = GetSmax(1.0, 1.0, Cd0, 0.2)
    Smax_E1z = GetSmax(1.0, 0.6, Cd0, 0.2)
    Smax_E2x = GetSmax(1.7, 1.0, Cd0, 0.2)
    Smax_E2z = GetSmax(1.7, 0.6, Cd0, 0.2)
    print("Smax_E1x = %.4f" % Smax_E1x)
    print("Smax_E1z = %.4f" % Smax_E1z)
    print("Smax_E2x = %.4f" % Smax_E2x)
    print("Smax_E2z = %.4f" % Smax_E2z)
    DES_E1x = GetDES(Smax_E1x, 0.40)
    DES_E1z = GetDES(Smax_E1z, 0.30)
    DES_E2x = GetDES(Smax_E2x, 0.40)
    DES_E2z = GetDES(Smax_E2z, 0.30)
    fig = plt.figure(figsize=(6, 3.75))
    ax = fig.add_axes([0.10, 0.14, 0.87, 0.82])
    ax.grid(True, ls='dotted')
    cv = FigureCanvas(fig)
    ax.set_xlabel('Period,T(s)')
    ax.set_ylabel('S')
    ax.plot(DES_E1x[0], DES_E1x[1], color='C1', ls='solid', linewidth=2.0, label="E1水平设计反应谱")
    ax.plot(DES_E1z[0], DES_E1z[1], color='C1', ls='dashed', linewidth=2.0, label="E1竖向设计反应谱")
    ax.plot(DES_E2x[0], DES_E2x[1], color='C0', ls='solid', linewidth=2.0, label="E2水平设计反应谱")
    ax.plot(DES_E2z[0], DES_E2z[1], color='C0', ls='dashed', linewidth=2.0, label="E2竖向设计反应谱")
    ax.legend(ncol=1)
    ax.set_xlim([0, 4.0])
    ax.set_ylim([0, 1.0])
    ax.set_xticklabels(ax.get_xticks(), rotation=90)
    ax.xaxis.set_major_locator(ticker.FixedLocator([0, 0.3, 0.4, 1, 2, 3, 4]))
    ax.yaxis.set_major_locator(ticker.FixedLocator([0, 0.1,  0.85, 0.7, Smax_E1z, Smax_E1x, Smax_E2z, Smax_E2x, ]))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    cv.print_figure('./out/设计反应谱.png', dpi=300)
    PrintSPD(DES_E1x[0], DES_E1x[1], "./out/E1水平设计反应谱.spd")
    PrintSPD(DES_E2x[0], DES_E2x[1], "./out/E2水平设计反应谱.spd")
