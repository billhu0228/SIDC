from src import GenSection, Superstructure
from src.bridge import StressInfo

if __name__ == "__main__":
    NU_MM = GenSection(721016.60, 7483.1945, 3.7064E+11, 929.95, 1070.05)
    NU_MM_CP = GenSection(1508516.6, 10813.1945, 9.3682E+11, 1566.8591, 433.1409, 733.1409)
    NU_ED = GenSection(2036334.755, 6440.8152, 6.8842E+11, 1008.132, 991.868)

    check_loc = 22.5
    info_pre = StressInfo(1860 * 0.75, 42 * 140, -633.04, -1269.9543)
    info_T1 = StressInfo(829, 1 * 12 * 140, -609.948, -1246.8591)
    info_T2 = StressInfo(829, 3 * 12 * 140, -369.948, -1006.8591)

    W9W4 = Superstructure([45, ] * 4, 70.0, 50.0)
    fcg0 = W9W4.Transfer(girder=0, loc=check_loc, sec=NU_MM, pre_stress=info_pre)
    fcg0 += W9W4.Erection(girder=0, loc=check_loc, sec=NU_MM, pre_stress=info_pre, fcg=fcg0)
    fcg0 += W9W4.Deck(girder=0, loc=check_loc, sec=NU_MM, pre_stress=info_pre, fcg=fcg0)
    dfcg0, fcg_TD1 = W9W4.Post1(girder=0, loc=check_loc, sec=NU_MM_CP, pre_stress=info_pre, T1_stress=info_T1, fcg=fcg0)
    fcg0 += dfcg0
    dfcg0, dfcg_T1 = W9W4.Deck2(girder=0, loc=check_loc, sec=NU_MM_CP, pre_stress=info_pre, T1_stress=info_T1, fcg=fcg0, fcg_T1=fcg_TD1)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    dfcg0, dfcg_T1, fcg_TD2 = W9W4.Post2(girder=0, loc=check_loc, sec=NU_MM_CP, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    dfcg0, dfcg_T1, dfcg_T2 = W9W4.DW(girder=0, loc=check_loc, sec=NU_MM_CP, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1, fcg_T2=fcg_TD2)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    fcg_TD2 += dfcg_T2
    dfcg0, dfcg_T1, dfcg_T2 = W9W4.LongTerm(sec=NU_MM_CP, pre_stress=info_pre, T1_stress=info_T1, T2_stress=info_T2, fcg=fcg0, fcg_T1=fcg_TD1, fcg_T2=fcg_TD2)
    fcg0 += dfcg0
    fcg_TD1 += dfcg_T1
    fcg_TD2 += dfcg_T2
