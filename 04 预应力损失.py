from typing import List
from scipy.optimize import bisect
import numpy as np
import scipy.optimize

import src as ss
from src import psi_creep, eps_shink
from src.tendon import Strand
from src.units import *
from src.mechanics import calculate


def fcpg(Pi, A, I, ec, Mg):
    A1 = Pi / A
    A2 = Pi * ec ** 2 / I
    A3 = Mg * ec / I
    return A1 + A2 - A3


def fcdp(Ms, Mw, I, Ic, ec, ybc, ybs):
    A1 = (Ms * ec) / I
    A2 = Mw * (ybc - ybs) / Ic
    return A1 + A2


class Bridge:
    def __int__(self, spans, g_beam, g_deck, g_w):
        return

    def fpe_pre(self, xi):
        return


def get_ec(strs: List['Strand'], xi):
    sum_ay = [a.get_yi(xi) * a.get_As(xi) for a in strs]
    sum_a = [a.get_As(xi) for a in strs]
    return sum(sum_ay) / sum(sum_a)


def get_area_all(strs: List['Strand'], xi):
    sum_a = [a.get_As(xi) for a in strs]
    return sum(sum_a)


def es_by_loss_ratio(loss_ratio, strands, xi, mom):
    loss = loss_ratio
    ec = get_ec(strands, xi, ) - ss.yb  # 629.4480  # 相对先张束偏心
    fpc = ss.fpc
    s_fcpg = fcpg(get_area_all(strands, xi) * fpc * (1 - loss), ss.A, ss.I, ec, mom)
    des = abs(196e3 / ss.Eci * s_fcpg)  # 弹性损失
    loss_check = des / fpc
    return loss_check - loss_ratio


def elastic_loss(L, strands, xi: float):
    eff_mat = calculate([L, ], dForce=[0, L], moment_loc=[xi, ])
    m_girder = eff_mat['m'][0] * 17.68 * 1e6  # Nmm , 简支状态自重跨中弯矩
    ret = bisect(es_by_loss_ratio, 0, 1, args=(strands, xi, m_girder))
    test = es_by_loss_ratio(ret, strands, xi, m_girder)
    ec = get_ec(strands, xi, ) - ss.yb  #
    s_fcpg = fcpg(get_area_all(strands, xi) * ss.fpc * (1 - ret), ss.A, ss.I, ec, m_girder)
    return ret * ss.fpc, s_fcpg


if __name__ == "__main__":
    N10 = Strand('N10', 75., 8, [0, 45], 140.0)
    N1a = Strand('N1a', 75., 4, [1.5, 45 - 1.5], 140.0)
    N1b = Strand('N1b', 75., 2, [3.0, 45 - 3.0], 140.0)
    N20 = Strand('N20', 125, 8, [0, 45], 140.0)
    N2a = Strand('N2a', 125, 4, [3, 45 - 3], 140.0)
    N2b = Strand('N2b', 125, 2, [4.5, 45 - 4.5], 140.0)
    N30 = Strand('N30', 175, 6, [0, 45], 140.0)
    N3b = Strand('N3b', 175, 2, [4.5, 45 - 4.5], 140.0)
    N40 = Strand('N40', 225, 2, [0, 45], 140.0)
    N50 = Strand('N40', 1955, 4, [0, 45], 140.0)

    Prestress = [N10, N1a, N1b, N20, N2a, N2b, N30, N3b, N40, N50]
    x = 0.5 * 45.0
    DEs, s_fcpg = elastic_loss(45.0, Prestress, x)
    print(DEs, s_fcpg)

    DSr = MPA((17 - 0.15 * 80) * 1000)  # 收缩损失，80% 相对湿度
    print(DSr)
# ec = get_ec(Prestress, x)
# Aps = get_area_all(Prestress, x)
# S = INCH(7483.1945)
# V = INCH(np.sqrt(721016.6002)) ** 2
# Kid = 1 + (ss.Ep / ss.Eci) * (Aps / ss.A) * (1 + (ss.A * ec ** 2 / ss.I)) * (
#         1 + 0.7 * psi_creep(36500, 7, 56, V, S, 80))
# Kid = 1 / Kid
# DCr = ss.Ep / ss.Eci * s_fcpg * psi_creep(100, 7, 56, V, S, 80) * Kid  # 徐变损失
# DSr = eps_shink(90, 56, V, S, 80) * ss.Ep * Kid  # 收缩
# Kdf = 1 + (ss.Ep / ss.Eci) * (Aps / ss.Ac) * (1 + (ss.Ac * ec ** 2 / ss.Ic)) * (
#         1 + 0.7 * psi_creep(36500, 7, 45, V, S, 80))
# Kdf = 1 / Kdf
# DSd = eps_shink(36400, 56, V, S, 80) * ss.Ep * Kdf  # 收缩
# DCd = ss.Ep / ss.Eci * s_fcpg * psi_creep(36500, 100, 56, V, S, 80) * Kdf  # 徐变损失
# print(DEs, s_fcpg)
# print(DSr)

# DR1 = 8.0
# DR2 = 8.0

#    eff = calculate([45, ], dForce=[0, 45], moment_loc=[45 * 0.5])

#    r4 = calculate([45, ] * 5, dForce=[0, 45 * 5.0], moment_loc=[45 * 0.5])

#

#
#    DR1 = 0.0
#    DR2 = MPA(0.3 * (20 - 0.4 * KSI(DEs) - 0.2 * KSI(DSr + DCr)) * 1e3)
#    DT = DEs + DSr + DCr + DR2
#    print(MPA(28500e3))
#    print(DEs / fpc)
#    print("Losses at Transfer : %.3f MPa (%.1f%%)" % (DEs, DEs / fpc * 100))
#    print("Losses at Service : %.3f MPa (%.1f%%)" % (DT, DT / fpc * 100))
#    print("Stress at Service : %.3f MPa" % (fpc - (DEs + DSr + DCr + DR2)))

#    loss_post = 0.1
#    fpc_post = 1860 * 0.8
#    s_fcpg_post = fcpg(-4 * 12 * 140 * fpc_post * (1 - loss_post), ss.Ac, ss.Ic, -775.33, Mg + Ms + Mw)
#    DEs_post = abs(196e3 / ss.Ec * s_fcpg_post)  # 弹性损失

#    print("Losses at Transfer of Post : %.3f MPa (%.1f%%)" % (DEs_post, DEs_post / fpc_post * 100))
#    DSr_post = MPA((17 - 0.15 * 80) * 1000)  # 收缩损失，80% 相对湿度

#    s_fcdp = fcdp(Ms, Mw, ss.I, ss.Ic, -ec, ss.ybc, ss.yb - ec)
#    DCr = MPA(12 * PSI(-s_fcpg) - 7 * PSI(s_fcdp))  # 徐变损失
