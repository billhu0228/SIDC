from src import GenSection, Superstructure
from src.bridge import StressInfo

if __name__ == "__main__":
    no_comp = GenSection(2036334.755, 6440.8152, 6.8842E+11, 1008.132, 991.868)
    comp = GenSection(2823834.7552, 9770.81, 1.4348E+12, 1326.5717, 673.4283, 973.4283)

    check_loc = 0.8
    info_pre = StressInfo(1860 * 0.75, 28 * 140, -618.132, -936.5717)
    info_T1 = StressInfo(829, 1 * 12 * 140, -458.132, 776.5717)
    info_T2 = StressInfo(829, 3 * 12 * 140, 341.868, 23.4283)

    W9W4 = Superstructure([45, ] * 4, 70.0, 50.0)
    fcg0 = W9W4.Transfer(girder=0, loc=check_loc, sec=no_comp, pre_stress=info_pre)
    fcg0 += W9W4.Erection(girder=0, loc=check_loc, sec=no_comp, pre_stress=info_pre, fcg=fcg0)
    fcg0 += W9W4.Deck(girder=0, loc=check_loc, sec=no_comp, pre_stress=info_pre, fcg=fcg0)
    dfcg0, fcg_TD1 = W9W4.Post1(girder=0, loc=check_loc, sec=comp, pre_stress=info_pre, T1_stress=info_T1, fcg=fcg0)
    fcg0 += dfcg0
    dfcg0, dfcg_T1 = W9W4.Deck2(girder=0, loc=check_loc, sec=comp, pre_stress=info_pre, T1_stress=info_T1, fcg=fcg0, fcg_T1=fcg_TD1)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    dfcg0, dfcg_T1, fcg_TD2 = W9W4.Post2(girder=0, loc=check_loc, sec=comp, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    dfcg0, dfcg_T1, dfcg_T2 = W9W4.DW(girder=0, loc=check_loc, sec=comp, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1, fcg_T2=fcg_TD2)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    fcg_TD2 += dfcg_T2
    dfcg0, dfcg_T1, dfcg_T2 = W9W4.LongTerm(sec=comp, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1, fcg_T2=fcg_TD2)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    fcg_TD2 += dfcg_T2
