import copy
from openseespy.opensees import *
from typing import List
import numpy as np


def get_node_force(n, dof, nmax):
    if n == nmax:
        return eleForce(nmax - 1)[dof + 2]
    else:
        return eleForce(n)[dof - 1]


def get_nodes_info(x: float, length: float, e_num: int):
    step = length / e_num
    ni = int(x / step) + 1
    nj = ni + 1
    xj = (x % step) / step
    xi = 1 - xj
    if x == length:
        return [[ni - 1, 0], [nj - 1, 1]]
    return [[ni, xi], [nj, xj]]


def calculate(span: List[int], cForce: List[float] = None,
              dForce=None, moment_loc=None, shear_loc=None,
              cForce_ft: List[float] = None,
              e_num: int = 1000, ):
    """
    计算连续梁内力
    :param cForce_ft:
    :param span: 跨境列表
    :param cForce: 集中力坐标
    :param dForce: 均布力作用范围
    :param moment_loc: 计算弯矩位置
    :param shear_loc: 计算剪力位置
    :param e_num: 单元划分数量，default=1000
    :return: 结果字典
    """
    # -----------------------------------------------------#
    res = {'m': [], 's': []}
    xmax = float(sum(span))
    step = xmax / e_num
    bearingNode = [1, ]
    for ii, x in enumerate(span):
        bearingNode.append(int(np.round(sum(span[0:ii + 1]) / step)) + 1)
    # -----------------------------------------------------#
    wipe()
    model('basic', '-ndm', 2, '-ndf', 3)
    for i in range(e_num + 1):
        node_num = i + 1
        xi = step * i
        if node_num in bearingNode:
            j = bearingNode.index(node_num)

            xi = float(sum(span[0:j]))
        node(node_num, xi, 0)
    for i in bearingNode:
        if i == 1:
            fix(i, 1, 1, 0)
        else:
            fix(i, 0, 1, 0)
    geomTransf('Linear', 1)
    for e in range(e_num):
        element('elasticBeamColumn', e + 1, e + 1, e + 2, 10, 1e4, 1e10, 1, 1)
        # element('ElasticTimoshenkoBeam', e + 1, e + 1, e + 2, 200e9, 200e9, 1, 1, 1, 1)
    timeSeries("Linear", 1)
    pattern("Plain", 1, 1)
    if cForce is not None:  # 施加集中力
        for kk, loc in enumerate(cForce):
            ft = cForce_ft[kk] if cForce_ft is not None else 1.0
            ser = get_nodes_info(loc, xmax, e_num)
            for force in ser:
                if force[0] > bearingNode[-1]:
                    continue
                load(force[0], 0, -force[1] * ft, 0)
    # sum_d = 0
    if dForce is not None:
        # for f_range in dForce:
        info0 = get_nodes_info(dForce[0], xmax, e_num)
        info1 = get_nodes_info(dForce[1], xmax, e_num)
        nn = info0[1][0]
        while nn < info1[0][0]:
            load(nn, 0, -step * 0.5, 0)
            load(nn + 1, 0, -step * 0.5, 0)
            nn += 1
            # sum_d += -step
        for info in [info0]:
            a = info[0][1]
            b = info[1][1]
            w = a * step
            aa = 0.5 * w / step
            bb = 1 - aa
            load(info[0][0], 0, -w * aa, 0)
            load(info[1][0], 0, -w * bb, 0)
            # sum_d += -w
        for info in [info1]:
            a = info[0][1]
            b = info[1][1]
            w = b * step
            bb = 0.5 * w / step
            aa = 1 - bb
            load(info[0][0], 0, -w * aa, 0)
            load(info[1][0], 0, -w * bb, 0)
            # sum_d += -w
    system("BandSPD")
    numberer("Plain")
    constraints("Plain")
    test('NormUnbalance', 1.0e-4, 50)
    # test('EnergyIncr', 1e-6, 50)
    integrator("LoadControl", 1.0)
    algorithm("Linear")
    analysis("Static")
    analyze(1)
    tmp = []
    if moment_loc is not None:
        for x in moment_loc:
            info = get_nodes_info(x, xmax, e_num)
            m0 = get_node_force(info[0][0], 3, e_num + 1)
            m1 = get_node_force(info[1][0], 3, e_num + 1)
            tmp.append(m0 * info[0][1] + m1 * info[1][1])
        res['m'] = copy.deepcopy(tmp)
    tmp = []
    if shear_loc is not None:
        for x in shear_loc:
            info = get_nodes_info(x, xmax, e_num)
            m0 = get_node_force(info[0][0], 2, e_num + 1)
            m1 = get_node_force(info[1][0], 2, e_num + 1)
            tmp.append(m0 * info[0][1] + m1 * info[1][1])
        res['s'] = copy.deepcopy(tmp)
    return res


if __name__ == "__main__":
    # result = calculate(span=[30],
    #                    cForce=[15],
    #                    dForce=[],
    #                    # moment_loc=[a for a in range(31)],
    #                    shear_loc=[a for a in range(31)],
    #                    )
    result2 = calculate(span=[45, ] * 4, cForce=[], dForce=[0, 180], moment_loc=[0, 22.5, 45])
    print(result2)
    f = 1
