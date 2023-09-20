from scipy.optimize import bisect
import src.common as ss
import src.creep as cr
import src.shrink as sh

from src.mechanics import calculate


class StressInfo:
    def __init__(self, fpc, apc, epc_ncp, epc_cp):
        self.data = [fpc, apc, epc_ncp, epc_cp]


class GenSection:
    def __init__(self, A: float, U: float, I: float, yb: float, yt: float, ydeck: float = None):
        self.A = A
        self.U = U
        self.h = 2 * A / U
        self.I = I
        self.yb = yb
        self.yt = yt
        self.ydeck = ydeck

    def pre_stress(self, pi, ec, y0):
        return pi / self.A + pi * ec / self.I * y0

    def mom_stress(self, mom, y0):
        return mom / self.I * y0


class Superstructure:
    def __init__(self, spans, fc_g, fc_deck, Rh=0.8):
        self.spans = spans
        self.fc_girder = fc_g
        self.fc_deck = fc_deck
        self.RH = Rh
        self.day_arr = [7, 180, 183, 183, 186, 186, 190, 10000]
        self.mid_ranges = []
        self.pier_ranges = []
        x0 = 0
        for sp in spans:
            x1 = x0 + sp
            self.mid_ranges.append([x0 + (sp - 20) * 0.5, x1 - (sp - 20) * 0.5])
            self.pier_ranges.append([x0, x0 + (sp - 20) * 0.5])
            self.pier_ranges.append([x1 - (sp - 20) * 0.5, x1])
            x0 = x1
        return

    def Transfer(self, girder, loc, sec, pre_stress: 'StressInfo', w_g=17.68e6):
        print("============  放张阶段  ============")
        fpc, apc, epc, epc_cp = pre_stress.data
        L = self.spans[girder]
        eff_mat = calculate([L, ], dForce=[0, L], moment_loc=[loc, ])
        m_girder = eff_mat['m'][0] * w_g  # Nmm , 简支状态自重跨中弯矩
        ret = bisect(self.es_by_loss_ratio, 0, 1, args=(sec, m_girder, fpc, apc, epc, ss.Eci))
        s_fcpg = sec.pre_stress(-fpc * apc * (1 - ret), epc, epc) + sec.mom_stress(m_girder, epc)
        fb = sec.pre_stress(-fpc * apc * (1 - ret), epc, -sec.yb) + sec.mom_stress(m_girder, -sec.yb)
        ft = sec.pre_stress(-fpc * apc * (1 - ret), epc, sec.yt) + sec.mom_stress(m_girder, sec.yt)
        f_t_rebar = sec.pre_stress(-fpc * apc * (1 - ret), epc, 949.868) + sec.mom_stress(m_girder, 949.868)
        print("%.1f | %.1f | %.1f " % (ft, fb, s_fcpg))
        print("弹性损失 %.1f MPa" % (ret * fpc))
        print("梁顶钢筋应力 %.1f MPa" % (f_t_rebar / ss.Eci * ss.Es))
        return s_fcpg

    def Erection(self, girder, loc, sec, pre_stress: 'StressInfo', fcg, w_g=17.68e6):
        print("============  架梁阶段  ============")
        _no, apc, epc, _no = pre_stress.data
        L = self.spans[girder]
        eff_mat = calculate([L, ], dForce=[0, L], moment_loc=[loc, ])
        m_girder = eff_mat['m'][0] * w_g  # Nmm , 简支状态自重跨中弯矩
        dsh, dcr = self.shrink_and_creep(self.day_arr[1], self.day_arr[0], fcg, sec, apc, epc)
        dpe = dsh + dcr
        s_fcpg = sec.pre_stress(dpe * apc, epc, epc)
        fb = sec.pre_stress(dpe * apc, epc, -sec.yb)
        ft = sec.pre_stress(dpe * apc, epc, sec.yt)
        print("%.1f | %.1f | %.1f " % (ft, fb, s_fcpg))
        print("收缩徐变损失(先张) %.1f MPa" % (dsh + dcr))
        return s_fcpg

    def Deck(self, girder, loc, sec, pre_stress: 'StressInfo', fcg, w_deck=26.52 * 1e6):
        print("============  跨中桥面板  ============")
        _no, apc, epc, _no = pre_stress.data
        L = self.spans[girder]
        range = [x - sum(self.spans[0:girder]) for x in self.mid_ranges[girder]]
        eff_mat = calculate([L, ], dForce=range, moment_loc=[loc, ])
        m_deck = eff_mat['m'][0] * w_deck  # Nmm , 简支状态自重跨中弯矩
        # m_deck = self.continues(w_deck, self.mid_ranges, sum(self.spans[0:girder]) + loc)
        dsh, dcr = self.shrink_and_creep(self.day_arr[2], self.day_arr[1], fcg, sec, apc, epc)
        dpe = dsh + dcr
        s_fcpg = sec.pre_stress(dpe * apc, epc, epc) + sec.mom_stress(m_deck, epc)
        fb = sec.pre_stress(dpe * apc, epc, -sec.yb) + sec.mom_stress(m_deck, -sec.yb)
        ft = sec.pre_stress(dpe * apc, epc, sec.yt) + sec.mom_stress(m_deck, sec.yt)
        print("%.1f | %.1f | %.1f " % (ft, fb, s_fcpg))
        print("收缩徐变损失(先张) %.1f MPa" % (dsh + dcr))
        return s_fcpg

    def Post1(self, girder, loc, sec, pre_stress: 'StressInfo', T1_stress: 'StressInfo', fcg, isNoCP, w_g=17.68e6, w_deck=26.52 * 1e6):
        print("============  第1批预应力  ============")
        if isNoCP:  # 按组合前截面计算
            _no, apc, epc, _no = pre_stress.data
            fpe_T1, apc_T1, epc_T1, _no = T1_stress.data
        else:
            _no, apc, _no, epc = pre_stress.data
            fpe_T1, apc_T1, _no, epc_T1 = T1_stress.data
        m_deck = self.continues(w_deck, self.mid_ranges, loc)
        L = self.spans[girder]
        eff_mat = calculate([L, ], dForce=[0, L], moment_loc=[loc, ])
        m_girder = eff_mat['m'][0] * w_g  # Nmm , 简支状态自重跨中弯矩
        dsh, dcr = self.shrink_and_creep(self.day_arr[3], self.day_arr[2], fcg, sec, apc, epc)
        desT1 = -sec.pre_stress(-fpe_T1 * apc_T1, epc_T1, epc) / ss.Ec * ss.Ep
        dpe = dsh + dcr + desT1
        s_fcpg = sec.pre_stress(dpe * apc, epc, epc) + sec.pre_stress(-fpe_T1 * apc_T1, epc_T1, epc)
        s_fcpg_T1 = sec.pre_stress(-fpe_T1 * apc_T1, epc_T1, epc_T1)
        fb = sec.pre_stress(dpe * apc, epc, -sec.yb) + sec.pre_stress(-fpe_T1 * apc_T1, epc_T1, -sec.yb)
        ft = sec.pre_stress(dpe * apc, epc, sec.yt) + sec.pre_stress(-fpe_T1 * apc_T1, epc_T1, sec.yt)
        if isNoCP:
            fdeck = 0
        else:
            fdeck = sec.pre_stress(dpe * apc, epc, sec.ydeck) + sec.pre_stress(-fpe_T1 * apc_T1, epc_T1, sec.ydeck)
        print("%.1f | %.1f | %.1f | %.1f | %.1f" % (ft, fb, fdeck, s_fcpg, s_fcpg_T1))
        print("弹性损失(先张) %.1f  MPa" % desT1)
        print("收缩徐变损失(先张) %.1f MPa" % (dsh + dcr))
        return s_fcpg, s_fcpg_T1

    def Deck2(self, girder, loc, sec, pre_stress: 'StressInfo', T1_stress: 'StressInfo', fcg, fcg_T1, isNoCP, w_g=17.68e6, w_deck=26.52 * 1e6):
        print("============ 墩顶桥面板  ============")
        if isNoCP:  # 按组合前截面计算
            _no, apc, epc, _no = pre_stress.data
            fpe_T1, apc_T1, epc_T1, _no = T1_stress.data
        else:
            _no, apc, _no, epc = pre_stress.data
            fpe_T1, apc_T1, _no, epc_T1 = T1_stress.data

        m_deck = self.continues(w_deck, self.pier_ranges, sum(self.spans[0:girder]) + loc)
        dsh, dcr = self.shrink_and_creep(self.day_arr[4], self.day_arr[3], fcg, sec, apc, epc)
        dpe = dsh + dcr
        dsh_T1, dcr_T1 = self.shrink_and_creep(self.day_arr[4], self.day_arr[3], fcg_T1, sec, apc_T1, epc_T1)
        dpe_T1 = dsh_T1 + dcr_T1
        s_fcpg = sec.pre_stress(dpe * apc, epc, epc) + sec.mom_stress(m_deck, epc)
        s_fcpg_T1 = sec.pre_stress(dpe_T1 * apc_T1, epc_T1, epc_T1) + sec.mom_stress(m_deck, epc_T1)
        fb = sec.pre_stress(dpe * apc, epc, -sec.yb) + sec.pre_stress(dpe_T1 * apc_T1, epc_T1,
                                                                      -sec.yb) + sec.mom_stress(m_deck, -sec.yb)
        ft = sec.pre_stress(dpe * apc, epc, sec.yt) + sec.pre_stress(dpe_T1 * apc_T1, epc_T1, sec.yt) + sec.mom_stress(m_deck, sec.yt)
        if isNoCP:
            fdeck = 0
        else:
            fdeck = sec.pre_stress(dpe * apc, epc, sec.ydeck) + sec.pre_stress(dpe_T1 * apc_T1, epc_T1, sec.ydeck)
        print("%.1f | %.1f | %.1f | %.1f | %.1f" % (ft, fb, fdeck, s_fcpg, s_fcpg_T1))
        print("收缩徐变损失(先张) %.1f  MPa" % (dsh + dcr))
        print("收缩徐变损失(后张T1) %.1f  MPa" % (dsh_T1 + dcr_T1))
        return s_fcpg, s_fcpg_T1

    def Post2(self, girder, loc, sec, pre_stress: 'StressInfo', T1_stress: 'StressInfo', T2_stress: 'StressInfo',
              fcg, fcg_T1, w_g=17.68e6, w_deck=26.52 * 1e6):
        print("============  第2批预应力  ============")
        _no, apc, _no, epc = pre_stress.data
        fpe_T1, apc_T1, _no, epc_T1 = T1_stress.data
        fpe_T2, apc_T2, _no, epc_T2 = T2_stress.data
        m_deck = self.continues(w_deck, self.mid_ranges, loc)
        L = self.spans[girder]
        eff_mat = calculate([L, ], dForce=[0, L], moment_loc=[loc, ])
        m_girder = eff_mat['m'][0] * w_g  # Nmm , 简支状态自重跨中弯矩
        dsh, dcr = self.shrink_and_creep(self.day_arr[5], self.day_arr[4], fcg, sec, apc, epc)
        desT2 = -sec.pre_stress(-fpe_T2 * apc_T2, epc_T2, epc) / ss.Ec * ss.Ep
        dpe = dsh + dcr + desT2
        dsh_T1, dcr_T1 = self.shrink_and_creep(self.day_arr[5], self.day_arr[4], fcg_T1, sec, apc_T1, epc_T1)
        desT2T1 = -sec.pre_stress(-fpe_T2 * apc_T2, epc_T2, epc_T1) / ss.Ec * ss.Ep
        dpeT1 = dsh_T1 + dcr_T1 + desT2T1
        s_fcpg = sec.pre_stress(dpe * apc, epc, epc) + sec.pre_stress(-fpe_T2 * apc_T2, epc_T2, epc)
        s_fcpg_T1 = sec.pre_stress(dpeT1 * apc_T1, epc_T1, epc_T1) + sec.pre_stress(-fpe_T2 * apc_T2, epc_T2, epc_T1)
        s_fcpg_T2 = sec.pre_stress(-fpe_T2 * apc_T2, epc_T2, epc_T2)
        fb = (sec.pre_stress(dpe * apc, epc, -sec.yb) +
              sec.pre_stress(dpeT1 * apc_T1, epc_T1, -sec.yb) +
              sec.pre_stress(-fpe_T2 * apc_T2, epc_T2, -sec.yb))
        ft = (sec.pre_stress(dpe * apc, epc, sec.yt) +
              sec.pre_stress(dpeT1 * apc_T1, epc_T1, sec.yt) +
              sec.pre_stress(-fpe_T2 * apc_T2, epc_T2, sec.yt))
        fdeck = (sec.pre_stress(dpe * apc, epc, sec.ydeck) +
                 sec.pre_stress(dpeT1 * apc_T1, epc_T1, sec.ydeck) +
                 sec.pre_stress(-fpe_T2 * apc_T2, epc_T2, sec.ydeck))
        print("%.1f | %.1f | %.1f | %.1f | %.1f | %.1f" % (ft, fb, fdeck, s_fcpg, s_fcpg_T1, s_fcpg_T2))
        print("弹性损失(先张) %.1f  MPa" % desT2)
        print("弹性损失(第1批后张) %.1f  MPa" % desT2T1)
        print("收缩徐变损失(先张) %.1f  MPa" % (dsh + dcr))
        print("收缩徐变损失(后张T1) %.1f  MPa" % (dsh_T1 + dcr_T1))
        return s_fcpg, s_fcpg_T1, s_fcpg_T2

    def DW(self, girder, loc, sec, pre_stress: 'StressInfo', T1_stress: 'StressInfo', T2_stress: 'StressInfo',
           fcg, fcg_T1, fcg_T2, w_g=17.68e6, DW=26.52 * 1e6):
        print("============ 二期  ============")
        _no, apc, _no, epc = pre_stress.data
        fpe_T1, apc_T1, _no, epc_T1 = T1_stress.data
        fpe_T2, apc_T2, _no, epc_T2 = T2_stress.data
        m_deck = self.continues(DW, [[0, sum(self.spans)], ], sum(self.spans[0:girder]) + loc)
        dsh, dcr = self.shrink_and_creep(self.day_arr[6], self.day_arr[5], fcg, sec, apc, epc)
        dpe = dsh + dcr
        dsh_T1, dcr_T1 = self.shrink_and_creep(self.day_arr[6], self.day_arr[5], fcg_T1, sec, apc_T1, epc_T1)
        dpe_T1 = dsh_T1 + dcr_T1
        dsh_T2, dcr_T2 = self.shrink_and_creep(self.day_arr[6], self.day_arr[5], fcg_T2, sec, apc_T2, epc_T2)
        dpe_T2 = dsh_T2 + dcr_T2
        s_fcpg = sec.pre_stress(dpe * apc, epc, epc) + sec.mom_stress(m_deck, epc)
        s_fcpg_T1 = sec.pre_stress(dpe_T1 * apc_T1, epc_T1, epc_T1) + sec.mom_stress(m_deck, epc_T1)
        s_fcpg_T2 = sec.pre_stress(dpe_T2 * apc_T2, epc_T2, epc_T2) + sec.mom_stress(m_deck, epc_T2)
        fb = (sec.pre_stress(dpe * apc, epc, -sec.yb) +
              sec.pre_stress(dpe_T1 * apc_T1, epc_T1, -sec.yb) +
              sec.pre_stress(dpe_T2 * apc_T2, epc_T2, -sec.yb) +
              sec.mom_stress(m_deck, -sec.yb))
        ft = (sec.pre_stress(dpe * apc, epc, sec.yt) +
              sec.pre_stress(dpe_T1 * apc_T1, epc_T1, sec.yt) +
              sec.pre_stress(dpe_T2 * apc_T2, epc_T2, sec.yt) +
              sec.mom_stress(m_deck, sec.yt))
        fdeck = (sec.pre_stress(dpe * apc, epc, sec.ydeck) +
                 sec.pre_stress(dpe_T1 * apc_T1, epc_T1, sec.ydeck) +
                 sec.pre_stress(dpe_T2 * apc_T2, epc_T2, sec.ydeck) +
                 sec.mom_stress(m_deck, sec.ydeck)
                 )
        print("%.1f | %.1f | %.1f | %.1f | %.1f | %.1f" % (ft, fb, fdeck, s_fcpg, s_fcpg_T1, s_fcpg_T2))
        print("收缩徐变损失(先张)   %.1f MPa" % (dsh + dcr))
        print("收缩徐变损失(后张T1) %.1f MPa" % (dsh_T1 + dcr_T1))
        print("收缩徐变损失(后张T2) %.1f MPa" % (dsh_T2 + dcr_T2))
        return s_fcpg, s_fcpg_T1, s_fcpg_T2

    def LongTerm(self, sec, pre_stress: 'StressInfo', T1_stress: 'StressInfo', T2_stress: 'StressInfo', fcg, fcg_T1, fcg_T2):
        print("============ 长期  ============")
        _no, apc, _no, epc = pre_stress.data
        fpe_T1, apc_T1, _no, epc_T1 = T1_stress.data
        fpe_T2, apc_T2, _no, epc_T2 = T2_stress.data
        dsh, dcr = self.shrink_and_creep(self.day_arr[7], self.day_arr[6], fcg, sec, apc, epc)
        dpe = dsh + dcr
        dsh_T1, dcr_T1 = self.shrink_and_creep(self.day_arr[7], self.day_arr[6], fcg_T1, sec, apc_T1, epc_T1)
        dpe_T1 = dsh_T1 + dcr_T1
        dsh_T2, dcr_T2 = self.shrink_and_creep(self.day_arr[7], self.day_arr[6], fcg_T2, sec, apc_T2, epc_T2)
        dpe_T2 = dsh_T2 + dcr_T2
        s_fcpg = sec.pre_stress(dpe * apc, epc, epc)
        s_fcpg_T1 = sec.pre_stress(dpe_T1 * apc_T1, epc_T1, epc_T1)
        s_fcpg_T2 = sec.pre_stress(dpe_T2 * apc_T2, epc_T2, epc_T2)
        fb = (sec.pre_stress(dpe * apc, epc, -sec.yb) +
              sec.pre_stress(dpe_T1 * apc_T1, epc_T1, -sec.yb) +
              sec.pre_stress(dpe_T2 * apc_T2, epc_T2, -sec.yb))
        ft = (sec.pre_stress(dpe * apc, epc, sec.yt) +
              sec.pre_stress(dpe_T1 * apc_T1, epc_T1, sec.yt) +
              sec.pre_stress(dpe_T2 * apc_T2, epc_T2, sec.yt))
        fdeck = (sec.pre_stress(dpe * apc, epc, sec.ydeck) +
                 sec.pre_stress(dpe_T1 * apc_T1, epc_T1, sec.ydeck) +
                 sec.pre_stress(dpe_T2 * apc_T2, epc_T2, sec.ydeck))
        print("%.1f | %.1f | %.1f | %.1f | %.1f | %.1f" % (ft, fb, fdeck, s_fcpg, s_fcpg_T1, s_fcpg_T2))
        print("收缩徐变损失(先张) %.1f    MPa" % (dsh + dcr))
        print("收缩徐变损失(后张T1) %.1f  MPa" % (dsh_T1 + dcr_T1))
        print("收缩徐变损失(后张T2) %.1f  MPa" % (dsh_T2 + dcr_T2))
        return s_fcpg, s_fcpg_T1, s_fcpg_T2

    def shrink_and_creep(self, t, t0, sigma0, section: 'GenSection', apc, epc):
        Kid = cr.Kid(t, t0, section.A, section.U, self.RH, self.fc_girder, ss.Ec, ss.Ep, section.I, apc, epc)
        CR_coff = cr.creep_coff(t, t0, section.A, section.U, self.RH, self.fc_girder)
        eps_sk = sh.shrink_eps(t, t0, self.fc_girder, 5, self.RH, section.A, section.U)
        shrink_loss = eps_sk * ss.Ep * Kid
        creep_loss = sigma0 / ss.Ec * CR_coff * ss.Ep * Kid
        return abs(shrink_loss), abs(creep_loss)

    def continues(self, uniload, ranges, loc):
        nn = len(ranges)
        mat = []
        for i in range(nn):
            mat.append(calculate(self.spans, dForce=ranges[i], moment_loc=[loc, ]))
        ret = sum([a['m'][0] for a in mat]) * uniload
        return ret

    @staticmethod
    def es_by_loss_ratio(loss_ratio: float, sect: 'GenSection', mom, fpc, apc, epc, Eci):
        s_fcpg = sect.pre_stress(-fpc * apc * (1 - loss_ratio), epc, epc) + sect.mom_stress(mom, epc)
        des = ss.Ep / Eci * s_fcpg  # 弹性损失
        loss_check = 1 - (fpc + des) / fpc
        return loss_check - loss_ratio
