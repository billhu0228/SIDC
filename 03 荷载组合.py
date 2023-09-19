import pandas as pd

from src.mechanics import calculate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pylab

# -------------------------------------------------------------------------------
# 绘图参数设置
# -------------------------------------------------------------------------------
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
pylab.mpl.rcParams['axes.unicode_minus'] = False
pylab.mpl.rcParams['font.size'] = 8
pylab.mpl.rcParams['legend.fontsize'] = u'small'
pylab.mpl.rcParams['xtick.labelsize'] = u'small'
pylab.mpl.rcParams['ytick.labelsize'] = u'small'


def get_lane(effect_matrix: pd.DataFrame, label: str, lane_factor):
    ret = effect_matrix[['x']].copy()
    ret[label + '_max'] = 0
    ret[label + '_min'] = 0
    for col in effect_matrix.columns:
        if col.startswith("my") or col.startswith('sfz'):
            ret[label + '_max'] += effect_matrix[col].where(effect_matrix[col] > 0, 0) * lane_factor
            ret[label + '_min'] += effect_matrix[col].where(effect_matrix[col] < 0, 0) * lane_factor
    return ret


def get_one(effect_matrix: pd.DataFrame, label: str, lane_factor):
    ret = effect_matrix[['x']].copy()
    ret[label + '_max'] = 0
    ret[label + '_min'] = 0
    for col in effect_matrix.columns:
        if col.startswith("my") or col.startswith('sfz'):
            ret[label + '_max'] = pd.concat([ret[label + '_max'], effect_matrix[col]], axis=1).max(axis=1)
            ret[label + '_min'] = pd.concat([ret[label + '_min'], effect_matrix[col]], axis=1).min(axis=1)
    ret[label + '_max'] = ret[label + '_max'] * lane_factor
    ret[label + '_min'] = ret[label + '_min'] * lane_factor
    return ret


if __name__ == "__main__":
    L = [45, ] * 4
    # xs = [0.5*a for a in range(sum(L*2) + 1)]
    xs = [a for a in range(sum(L) + 1)]
    res = {'x': xs}
    r = calculate(L, dForce=[0, sum(L)], moment_loc=xs, shear_loc=xs)
    res['DC'] = np.array(r['m']) * (17.68 + 24.70 + 3.69) * 1e3
    res['DW'] = np.array(r['m']) * 9.22 * 1e3

    xs = [a for a in range(sum(L) + 1)]
    e_mat = {'x': xs}
    for x in xs:
        r = calculate(L, cForce=[x], moment_loc=xs, shear_loc=xs)
        e_mat['my_%i' % x] = r['m']
    e_mat = pd.DataFrame(e_mat)  # 均布荷载影响矩阵

    truck_mat = {'x': xs}
    for x in xs:
        r = calculate(L, cForce=[x, x + 4.3, x + 4.3 + 9.1], cForce_ft=[7. / 29.0, 1., 1.], moment_loc=xs, shear_loc=xs)
        truck_mat['my_%i' % x] = r['m']
    truck_mat = pd.DataFrame(truck_mat)  # Truck荷载影响矩阵

    td_mat = {'x': xs}
    for x in xs:
        r = calculate(L, cForce=[x, x + 1.2], moment_loc=xs, shear_loc=xs)
        td_mat['my_%i' % x] = r['m']
    td_mat = pd.DataFrame(td_mat)  # TD荷载影响矩阵

    la = get_lane(e_mat, 'LANE', 9.34e3)
    tr = get_one(truck_mat, 'TRUCK', 145e3)
    td = get_one(td_mat, 'TD', 110e3)
    res['Lane-max'] = la['LANE_max']
    res['Lane-min'] = la['LANE_min']
    res['Td-max'] = td['TD_max']
    res['Td-min'] = td['TD_min']
    res['Truck-max'] = tr['TRUCK_max']
    res['Truck-min'] = tr['TRUCK_min']
    res['LL-max'] = res['Lane-max'] + pd.concat([res['Td-max'], res['Truck-max']], axis=1).max(axis=1)
    res['LL-min'] = res['Lane-min'] + pd.concat([res['Td-min'], res['Truck-min']], axis=1).min(axis=1)
    res = pd.DataFrame(res)
    res.to_csv('f1.csv')
    f = 1
