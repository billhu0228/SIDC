import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)


def stress_cons(filename):
    data = pd.read_excel(filename, skiprows=1, usecols="C,F,I,J,L,Q:U")
    consider = ['钢束放张', '架梁', '桥面湿重', '二期']
    for stage in consider:
        msk1 = data['阶段'] == stage
        msk2 = data['截面位置'] == 1
        s_data = data[msk1 & msk2].iloc[:, 6:10]
        s_max = s_data.max().max()
        s_min = s_data.min().min()
        try:
            assert s_max <= 1.38 and s_min >= -31.2
        except AssertionError:
            print("施工阶段应力超限")
        print("%.1f\t%.1f" % (s_min, s_max))
        # break


def stress_service_1(filename):
    data = pd.read_excel(filename, skiprows=1, usecols="C,E,I,Q:U")
    consider = ['Service-1A', 'Service-1B(最小)', 'Service-1C(最小)']
    for stage in consider:
        msk1 = data['荷载'] == stage
        msk2 = data['截面位置'] == 1
        msk3 = data['截面位置'] == 2
        s_data = data[msk1 & msk2].iloc[:, 4:8]
        s_min_girder = s_data.min().min()
        s_data = data[msk1 & msk3].iloc[:, 4:8]
        s_min_slab = s_data.min().min()
        result = s_min_girder >= -26 and s_min_slab >= -20
        if result:
            res_str = "O.K."
        else:
            res_str = "Fail!"
        print("%.1f\t%.1f\t%s" % (s_min_girder, s_min_slab, res_str))


def stress_service_3(filename):
    data = pd.read_excel(filename, skiprows=1, usecols="C,E,I,Q:U")
    consider = ['Service-3(最大)']
    for stage in consider:
        msk1 = data['荷载'] == stage
        msk2 = data['截面位置'] == 1
        msk3 = data['截面位置'] == 2
        s_data = data[msk1 & msk2].iloc[:, 4:8]
        s_max_girder = s_data.max().max()
        s_min_girder = s_data.min().min()
        result = s_max_girder <= 2.09
        if result:
            res_str = "O.K."
        else:
            res_str = "Fail!"
        print("%.1f\t%s\t%s" % (s_max_girder, s_min_girder, res_str))


def principal_tensile_s3(filename, A, I, b, y):
    data = pd.read_excel(filename, skiprows=1, usecols="C,H,I,K:M")
    sig_x = data.iloc[:, 3] / (A * 1e6)
    sig_x += data.iloc[:, 4] / (I * 1e12) * (y * 1e3)
    print("%.1f"%(sig_x.max()))


if __name__ == '__main__':
    # 40m 简支
    # stress_cons(r"H:\20230830 萨马尔项目\01 上部结构计算\01 简支梁计算\S40梁单元应力CLS.xls")
    stress_service_1(r"H:\20230830 萨马尔项目\01 上部结构计算\01 简支梁计算\S40梁单元应力SLS.xls")
    stress_service_3(r"H:\20230830 萨马尔项目\01 上部结构计算\01 简支梁计算\S40梁单元应力SLS.xls")
    principal_tensile_s3(r"H:\20230830 萨马尔项目\01 上部结构计算\01 简支梁计算\S40梁单元内力Service3.xls", 1.511, 0.934, 0.225, 1.150)

    # 33m 简支
    # stress_cons(r"H:\20230830 萨马尔项目\01 上部结构计算\01 简支梁计算\S33梁单元应力CLS.xls")
    stress_service_1(r"H:\20230830 萨马尔项目\01 上部结构计算\01 简支梁计算\S33梁单元应力SLS.xls")
    stress_service_3(r"H:\20230830 萨马尔项目\01 上部结构计算\01 简支梁计算\S33梁单元应力SLS.xls")

   #  print(p)
