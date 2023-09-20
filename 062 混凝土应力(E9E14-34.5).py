from src import GenSection, Superstructure
from src.bridge import StressInfo

if __name__ == "__main__":
    # E13~EA 35米桥台截面
    no_comp = GenSection(2036334.755, 6440.8152, 6.8842E+11, 1008.132, 991.868)
    comp = GenSection(2823834.7552, 9770.81, 1.4348E+12, 1326.5717, 673.4283, 973.4283)

    gn = 4
    check_loc = 34.5
    info_pre = StressInfo(1860 * 0.75, 24 * 140, -586.4653, -904.905)
    info_T1 = StressInfo(829, 1 * 12 * 140, -458.132, -776.5717)
    info_T2 = StressInfo(829, 3 * 12 * 140, 341.868, 23.4283)

    W9W4 = Superstructure([45, ] * 4 + [35, ], 70.0, 50.0)
    fcg0 = W9W4.Transfer(girder=gn, loc=check_loc, sec=no_comp, pre_stress=info_pre)
    fcg0 += W9W4.Erection(girder=gn, loc=check_loc, sec=no_comp, pre_stress=info_pre, fcg=fcg0)
    fcg0 += W9W4.Deck(girder=gn, loc=check_loc, sec=no_comp, pre_stress=info_pre, fcg=fcg0)
    dfcg0, fcg_TD1 = W9W4.Post1(girder=gn, loc=check_loc, sec=no_comp, pre_stress=info_pre, T1_stress=info_T1, fcg=fcg0, isNoCP=True)
    fcg0 += dfcg0
    dfcg0, dfcg_T1 = W9W4.Deck2(girder=gn, loc=check_loc, sec=no_comp, pre_stress=info_pre, T1_stress=info_T1, fcg=fcg0, fcg_T1=fcg_TD1, isNoCP=True)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    dfcg0, dfcg_T1, fcg_TD2 = W9W4.Post2(girder=gn, loc=check_loc, sec=comp, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    dfcg0, dfcg_T1, dfcg_T2 = W9W4.DW(girder=gn, loc=check_loc, sec=comp, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1, fcg_T2=fcg_TD2)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    fcg_TD2 += dfcg_T2
    dfcg0, dfcg_T1, dfcg_T2 = W9W4.LongTerm(sec=comp, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1, fcg_T2=fcg_TD2)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    fcg_TD2 += dfcg_T2
