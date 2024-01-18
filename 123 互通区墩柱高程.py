import datetime

import ezdxf
import pandas as pd
from ezdxf.enums import TextEntityAlignment
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.math import Vec2
from srbpy import Align
import numpy as np
from PyAngle import Angle
from src.beam import Beam, connect


def get_control_line(M: Align, station: float, degree):
    cc = Vec2(M.get_coordinate(station))
    # deg = row['基础转角']
    ux = Vec2(M.get_direction(station))
    uy = ux.rotate(Angle.from_degrees(degree).to_rad())
    ux = uy.rotate(Angle.from_degrees(-90.0).to_rad())
    p0 = cc + uy * 10
    p1 = cc - uy * 10
    return p1, cc, p0


def get_piles_co(M: Align, station: float, degree, distance: float, ct_type: 'str'):
    cc = Vec2(M.get_coordinate(station))
    # deg = row['基础转角']
    ux = Vec2(M.get_direction(station))
    uy = ux.rotate(Angle.from_degrees(degree).to_rad())
    ux = uy.rotate(Angle.from_degrees(-90.0).to_rad())
    p0 = cc + uy * distance
    dx = []
    dy = []
    res = []
    if ct_type == "CP1":
        dx = [-2.25, 2.25]
        dy = [-2.25, 2.25]
    elif ct_type == "CP4":
        dx = [-2.25, 2.25]
        dy = [-4.5, 0, 4.5]
    elif ct_type == "CP5":
        dx = [-2.25, 2.25]
        dy = [-5.69, 0, 5.69]
    for yy in dy:
        for xx in dx:
            point = p0 + ux * xx + uy * yy
            res.append(point)
    return res


if __name__ == '__main__':
    D1 = Align('D1', './Data/EI/D1')
    D2 = Align('D2', './Data/EI/D2')
    D3 = Align('D3', './Data/EI/D3')
    D4 = Align('D4', './Data/EI/D4')
    M = Align('M', './Data/EI/M')
    CL_dic = {
        'D1': D1,
        'D2': D2,
        'D3': D3,
        'D4': D4,
        'M': M,
    }
    result = []
    text = []
    data = pd.read_excel("./Data/互通基础参数表-R02.xlsx", '承台参数')
    for i, row in data.iterrows():
        if not np.isnan(row['桩号']):
            st = row["桩号"]
            CL: Align = CL_dic[row['线位']]
            deg = row['基础转角']

