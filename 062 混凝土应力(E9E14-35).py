from src import GenSection, Superstructure
from src.bridge import StressInfo

if __name__ == "__main__":
    # E13~EA 35米跨中
    no_comp = GenSection(721016.60, 7483.1945, 3.7064E+11, 929.95, 1070.05)
    comp = GenSection(1508516.6, 10813.1945, 9.3682E+11, 1566.8591, 433.1409, 733.1409)

    gn = 4
    check_loc = 17.5
    info_pre2 = StressInfo(1860 * 0.75, 42 * 140, -633.0432, -1269.9543)
    info_pre = StressInfo(1860 * 0.75, 38 * 140, -622.8427, -1259.7538)
    info_T1 = StressInfo(1344, 1 * 12 * 140, -609.948, -1246.8591)
    info_T2 = StressInfo(1344, 3 * 12 * 140, -369.948, -1006.8591)

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
