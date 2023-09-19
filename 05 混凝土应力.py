import numpy as np

import src as ss
from src.units import *
from src.mechanics import calculate


def continues(spans, uniload, ranges, loc):
    nn = len(ranges)
    mat = []
    for i in range(nn):
        mat.append(calculate(spans, dForce=ranges[i], moment_loc=[loc, ]))
    ret = sum([a['m'][0] for a in mat]) * uniload
    return ret


if __name__ == "__main__":
    L = 45.0
    xi = 0.5 * L
    eff_mat = calculate([L, ], dForce=[0, L], moment_loc=[xi, ])
    m_girder = eff_mat['m'][0] * 17.68 * 1e6  # Nmm , 简支状态自重跨中弯矩
    ec = 633.0452380952381
    ec_T1_comp = 1246.86
    ec_T2_comp = 1006.86
    ec_T1_nc = 606.95

    SlabFirst = 20

    spans = [45, ] * 5
    load_ranges = [
        [12.5 + 45 * 0, 32.5 + 45 * 0],
        [12.5 + 45 * 1, 32.5 + 45 * 1],
        [12.5 + 45 * 2, 32.5 + 45 * 2],
        [12.5 + 45 * 3, 32.5 + 45 * 3],
        [12.5 + 45 * 4, 32.5 + 45 * 4],
    ]
    load_ranges2 = [
        [0, 12.5],
        [32.5 + 45 * 0, 57.5 + 45 * 0],
        [32.5 + 45 * 1, 57.5 + 45 * 1],
        [32.5 + 45 * 2, 57.5 + 45 * 2],
        [32.5 + 45 * 3, 57.5 + 45 * 3],
        [32.5 + 45 * 4, 225],
    ]

    fcc = KSI(45.0)
    t = 0.0948 * np.sqrt(fcc)
    print("放张")
    Pi = 140 * 1332 * 42
    ft = -Pi / ss.A + Pi * ec / ss.St - abs(m_girder) / ss.St
    fb = -Pi / ss.A - Pi * ec / ss.Sb + abs(m_girder) / ss.Sb
    fcg = -Pi / ss.A - Pi * ec / (ss.I / ec) + abs(m_girder) / (ss.I / ec)
    print(ft, fb, fcg)

    print("架梁")
    Pi = 140 * 1263.5 * 42
    ft = -Pi / ss.A + Pi * ec / ss.St - abs(m_girder) / ss.St
    fb = -Pi / ss.A - Pi * ec / ss.Sb + abs(m_girder) / ss.Sb
    fcg = -Pi / ss.A - Pi * ec / (ss.I / ec) + abs(m_girder) / (ss.I / ec)
    print("%.1f  ,  %.1f  ,  %.1f" % (ft, fb, fcg))

    print("跨中桥面板")
    Pi = 140 * 1252.7 * 42
    slab20 = continues(spans, 26.52 * 1e6, load_ranges, 22.5)
    ft = -Pi / ss.A + Pi * ec / ss.St - (abs(m_girder) + abs(slab20)) / ss.St
    fb = -Pi / ss.A - Pi * ec / ss.Sb + (abs(m_girder) + abs(slab20)) / ss.Sb
    fcg = -Pi / ss.A - Pi * ec / (ss.I / ec) + (abs(m_girder) + abs(slab20)) / (ss.I / ec)
    print("%.1f  ,  %.1f  ,  %.1f" % (ft, fb, fcg))

    print("第一批预应力")
    Pi = 140 * 1248.6 * 42
    Po = 12 * 140 * 829
    ft_g_by_post = (-Pi / ss.A + Pi * ec / ss.St - (abs(m_girder) + abs(slab20)) / ss.St -
                    Po / ss.Ac + Po * ec_T1_comp / ss.Stg)
    fb_by_post = (-Pi / ss.A - Pi * ec / ss.Sb + (abs(m_girder) + abs(slab20)) / ss.Sb -
                  Po / ss.Ac - Po * ec_T1_comp / ss.Sbc)
    ft_slab = -Po / ss.Ac + Po * ec_T1_comp / ss.Stc
    # fcg = -Pi / ss.A - Pi * ec / (ss.I / ec) + (abs(m_girder) + abs(slab20)) / (ss.I / ec)
    fcg_post = -Po / ss.Ac + Po * 23.1 ** 2 / ss.Ic
    print("%.1f  ,  %.1f  ,  %.1f  ,  %.1f" % (ft_g_by_post, fb_by_post, ft_slab, fcg_post))

    print("墩顶25m")
    Pi = 140 * 1241.3 * 42
    Po = 12 * 140 * 821.8
    slabtop = continues(spans, 26.52 * 1e6, load_ranges2, 22.5)

    ftg_by_slab = (-Pi / ss.A + Pi * ec / ss.St - (abs(m_girder) + abs(slab20)) / ss.St -
                   Po / ss.Ac + Po * ec_T1_comp / ss.Stg) + slabtop / ss.Stg
    fb_by_slab = (-Pi / ss.A - Pi * ec / ss.Sb + (abs(m_girder) + abs(slab20)) / ss.Sb -
                  Po / ss.Ac - Po * ec_T1_comp / ss.Sbc) - slabtop / ss.Sbc
    ft_by_slab = -Po / ss.Ac + Po * ec_T1_comp / ss.Stc + slabtop / ss.Stc
    fcg_slab = -Po / ss.Ac + Po * 23.1 ** 2 / ss.Ic - slabtop / ss.Ic * 1269.95

    print("%.1f  ,  %.1f  ,  %.1f   ,%.1f  " % (ftg_by_slab, fb_by_slab, ft_by_slab, fcg_slab))

    print("第二批预应力")
    Pi = 140 * 1230.4 * 42
    Po1 = 12 * 140 * 810.6 * 1
    Po2 = 12 * 140 * 829.0 * 3

    ftg_by_slab = ((-Pi / ss.A + Pi * ec / ss.St - (abs(m_girder) + abs(slab20)) / ss.St -
                    Po1 / ss.Ac + Po1 * ec_T1_comp / ss.Stg -
                    Po2 / ss.Ac + Po2 * ec_T2_comp / ss.Stg) +
                   slabtop / ss.Stg)

    fb_by_slab = ((-Pi / ss.A - Pi * ec / ss.Sb + (abs(m_girder) + abs(slab20)) / ss.Sb -
                   Po1 / ss.Ac - Po1 * ec_T1_comp / ss.Sbc -
                   Po2 / ss.Ac - Po2 * ec_T2_comp / ss.Sbc) -
                  slabtop / ss.Sbc)
    ft_by_slab = (-Po1 / ss.Ac + Po1 * ec_T1_comp / ss.Stc
                  - Po2 / ss.Ac + Po2 * ec_T2_comp / ss.Stc
                  + slabtop / ss.Stc)
    fcg_slab = (-Po1 / ss.Ac + Po1 * 23.1 ** 2 / ss.Ic
                - Po2 / ss.Ac + Po2 * 263.1 ** 2 / ss.Ic
                - slabtop / ss.Ic * 1269.95)

    fcg_po2 = - Po2 / ss.Ac + Po2 * 263.1 ** 2 / ss.Ic
    fpo1_po2 = - Po2 / ss.Ac + Po2 * 240 ** 2 / ss.Ic

    print("%.1f  ,  %.1f  ,  %.1f   ,%.1f  " % (ftg_by_slab, fb_by_slab, ft_by_slab, fcg_slab))

    print("二期")
    DW = continues(spans, 9.22 * 1e6, load_ranges2, 22.5)
    Pi = 140 * 1222.9 * 42
    Po1 = 12 * 140 * 808.1 * 1
    Po2 = 12 * 140 * 826.5 * 3
    ftg_by_slab = ((-Pi / ss.A + Pi * ec / ss.St - (abs(m_girder) + abs(slab20) + abs(DW)) / ss.St -
                    Po1 / ss.Ac + Po1 * ec_T1_comp / ss.Stg -
                    Po2 / ss.Ac + Po2 * ec_T2_comp / ss.Stg) +
                   slabtop / ss.Stg)

    fb_by_slab = ((-Pi / ss.A - Pi * ec / ss.Sb + (abs(m_girder) + abs(slab20) + abs(DW)) / ss.Sb -
                   Po1 / ss.Ac - Po1 * ec_T1_comp / ss.Sbc -
                   Po2 / ss.Ac - Po2 * ec_T2_comp / ss.Sbc) -
                  slabtop / ss.Sbc)
    ft_by_slab = (-Po1 / ss.Ac + Po1 * ec_T1_comp / ss.Stc
                  - Po2 / ss.Ac + Po2 * ec_T2_comp / ss.Stc
                  + (slabtop - abs(DW)) / ss.Stc)
    fcg_slab = (-Po1 / ss.Ac + Po1 * 23.1 ** 2 / ss.Ic
                - Po2 / ss.Ac + Po2 * 263.1 ** 2 / ss.Ic
                - slabtop / ss.Ic * 1269.95
                + abs(DW) / ss.Ic * 1269.95
                )
    print("%.1f  ,  %.1f  ,  %.1f   ,%.1f  " % (ftg_by_slab, fb_by_slab, ft_by_slab, fcg_slab))

    print("运营")
    DW = continues(spans, 9.22 * 1e6, load_ranges2, 22.5)
    Pi = 140 * 1187.8 * 42
    Po1 = 12 * 140 * 768 * 1
    Po2 = 12 * 140 * 786.4 * 3
    ftg_by_slab = ((-Pi / ss.A + Pi * ec / ss.St - (abs(m_girder) + abs(slab20) + abs(DW)) / ss.St -
                    Po1 / ss.Ac + Po1 * ec_T1_comp / ss.Stg -
                    Po2 / ss.Ac + Po2 * ec_T2_comp / ss.Stg) +
                   slabtop / ss.Stg)

    fb_by_slab = ((-Pi / ss.A - Pi * ec / ss.Sb + (abs(m_girder) + abs(slab20) + abs(DW)) / ss.Sb -
                   Po1 / ss.Ac - Po1 * ec_T1_comp / ss.Sbc -
                   Po2 / ss.Ac - Po2 * ec_T2_comp / ss.Sbc) -
                  slabtop / ss.Sbc)
    ft_by_slab = (-Po1 / ss.Ac + Po1 * ec_T1_comp / ss.Stc
                  - Po2 / ss.Ac + Po2 * ec_T2_comp / ss.Stc
                  + (slabtop - abs(DW)) / ss.Stc)
    fcg_slab = (-Po1 / ss.Ac + Po1 * 23.1 ** 2 / ss.Ic
                - Po2 / ss.Ac + Po2 * 263.1 ** 2 / ss.Ic
                - slabtop / ss.Ic * 1269.95
                + abs(DW) / ss.Ic * 1269.95
                )
    print("%.1f  ,  %.1f  ,  %.1f   ,%.1f  " % (ftg_by_slab, fb_by_slab, ft_by_slab, fcg_slab))
