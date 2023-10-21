import pandas as pd

from src import GenSection, Superstructure
from src.bridge import StressInfo

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.options.display.float_format = '{:,.1f}'.format
    # E13~EA 35米跨中
    no_comp = GenSection(721016.60, 7483.1945, 3.7064E+11, 929.95, 1070.05)
    comp = GenSection(1508516.6, 10813.1945, 9.3682E+11, 1566.8591, 433.1409, 733.1409)

    end_no_comp = GenSection(2036334.755, 6440.8152, 6.8842E+11, 1008.132, 991.868)
    end_comp = GenSection(2823834.7552, 9770.81, 1.4348E+12, 1326.5717, 673.4283, 973.4283)

    gn = 4
    check_loc = 17.5
    info_pre = StressInfo(1860 * 0.75, 38 * 140, -622.8427, -1259.7538)
    info_T1 = StressInfo(1344, 1 * 12 * 140, -609.948, -1246.8591)
    info_T2 = StressInfo(1344, 3 * 12 * 140, -369.948, -1006.8591)

    end_info_pre = StressInfo(1860 * 0.75, 24 * 140, -586.4653, -904.905)
    end_info_T1 = StressInfo(967, 1 * 12 * 140, -458.132, -776.5717)
    end_info_T2 = StressInfo(967, 3 * 12 * 140, 341.868, 23.4283)

    pier_info_pre = StressInfo(1860 * 0.75, 24 * 140, -539.6105, -1176.5216)
    pier_info_T1 = StressInfo(967, 1 * 12 * 140, 410.052, -226.8591)
    pier_info_T2 = StressInfo(967, 3 * 12 * 140, 783.3853, 146.4742)

    Girders = Superstructure([45, ] * 4 + [35, ], 70.0, 50.0, pr_detail=False)

    print("---------------- C01 ----------------")
    r1 = Girders.check_stress(girder_n=0, location=0.5, non_cp_sec=no_comp, cp_section=comp,
                              pre_stress=StressInfo(1395, 24 * 140, -586.4653, -904.905),
                              post_str_1=StressInfo(1581, 1 * 12 * 140, -458.132, -776.5717),
                              post_str_2=StressInfo(1581, 3 * 12 * 140, 341.868, 23.4283),
                              isMiddle=False)
    print(r1)
    print("---------------- C02 ----------------")
    r1 = Girders.check_stress(girder_n=0, location=22.5, non_cp_sec=no_comp, cp_section=comp,
                              pre_stress=StressInfo(1395, 38 * 140, -622.8427, -1259.7538),
                              post_str_1=StressInfo(1578, 1 * 12 * 140, -609.948, -1246.8591),
                              post_str_2=StressInfo(1578, 3 * 12 * 140, -369.948, -1006.8591),
                              isMiddle=True)
    print(r1)
    print("---------------- C03 ----------------")
    r1 = Girders.check_stress(girder_n=0, location=44.5, non_cp_sec=end_no_comp, cp_section=end_comp,
                              pre_stress=StressInfo(1395, 24 * 140, -539.6105, -1176.5216),
                              post_str_1=StressInfo(1574, 1 * 12 * 140, 410.052, -226.8591),
                              post_str_2=StressInfo(1574, 3 * 12 * 140, 783.3853, 146.4742),
                              isMiddle=False)
    print(r1)

    print("---------------- C05 ----------------")
    r1 = Girders.check_stress(girder_n=2, location=0.5, non_cp_sec=no_comp, cp_section=comp,
                              pre_stress=StressInfo(1395, 24 * 140, -586.4653, -904.905),
                              post_str_1=StressInfo(1561, 1 * 12 * 140, -458.132, -776.5717),
                              post_str_2=StressInfo(1561, 3 * 12 * 140, 341.868, 23.4283),
                              isMiddle=False)
    print(r1)
    print("---------------- C06 ----------------")
    r1 = Girders.check_stress(girder_n=2, location=22.5, non_cp_sec=no_comp, cp_section=comp,
                              pre_stress=StressInfo(1395, 38 * 140, -622.8427, -1259.7538),
                              post_str_1=StressInfo(1555, 1 * 12 * 140, -609.948, -1246.8591),
                              post_str_2=StressInfo(1555, 3 * 12 * 140, -369.948, -1006.8591),
                              isMiddle=True)
    print(r1)
    print("---------------- C07 ----------------")
    r1 = Girders.check_stress(girder_n=2, location=44.5, non_cp_sec=end_no_comp, cp_section=end_comp,
                              pre_stress=StressInfo(1395, 24 * 140, -539.6105, -1176.5216),
                              post_str_1=StressInfo(1561, 1 * 12 * 140, 410.052, -226.8591),
                              post_str_2=StressInfo(1561, 3 * 12 * 140, 783.3853, 146.4742),
                              isMiddle=False)
    print(r1)

    print("---------------- C09 ----------------")
    r1 = Girders.check_stress(girder_n=4, location=0.5, non_cp_sec=no_comp, cp_section=comp,
                              pre_stress=StressInfo(1395, 24 * 140, -539.6105, -1176.5216),
                              post_str_1=StressInfo(1573, 1 * 12 * 140, 410.052, -226.8591),
                              post_str_2=StressInfo(1573, 3 * 12 * 140, 783.3853, 146.4742),
                              isMiddle=False)
    print(r1)
    print("---------------- C10 ----------------")
    r1 = Girders.check_stress(girder_n=4, location=17.5, non_cp_sec=no_comp, cp_section=comp,
                              pre_stress=StressInfo(1395, 38 * 140, -622.8427, -1259.7538),
                              post_str_1=StressInfo(1578, 1 * 12 * 140, -609.948, -1246.8591),
                              post_str_2=StressInfo(1578, 3 * 12 * 140, -369.948, -1006.8591),
                              isMiddle=True)
    print(r1)
    print("---------------- C11 ----------------")
    r1 = Girders.check_stress(girder_n=4, location=34.5, non_cp_sec=end_no_comp, cp_section=end_comp,
                              pre_stress=StressInfo(1395, 24 * 140, -586.4653, -904.905),
                              post_str_1=StressInfo(1581, 1 * 12 * 140, -458.132, -776.5717),
                              post_str_2=StressInfo(1581, 3 * 12 * 140, 341.868, 23.4283),
                              isMiddle=False)
    print(r1)
