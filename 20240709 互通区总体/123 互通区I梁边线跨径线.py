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
    p0 = cc + uy * 18
    p1 = cc - uy * 18
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
    D1 = Align('D1', '../Data/EI/D1')
    D2 = Align('D2', '../Data/EI/D2')
    D3 = Align('D3', '../Data/EI/D3')
    D4 = Align('D4', '../Data/EI/D4')
    M = Align('Mai', '../Data/EI/M')
    CL_dic = {
        'D1': D1,
        'D2': D2,
        'D3': D3,
        'D4': D4,
        'M': M,
    }
    al = D3
    st = 332
    ed = 372
    pt = 21
    stations = np.linspace(st, ed, pt, True)
    doc = ezdxf.new()
    msp = doc.modelspace()
    for ss in stations:
        ss_name = f"{ss:.3f}"
        ly = doc.layers.new(ss_name)
        ly.color = 50
        cc = Vec2(al.get_coordinate(ss))
        ux = Vec2(al.get_direction(ss))
        uy = ux.rotate_deg(90.0)
        p1 = cc - uy * 50
        p2 = cc + uy * 50
        msp.add_line(p1, p2, dxfattribs=GfxAttribs(layer=ss_name))

    now = datetime.date.today()
    doc.saveas("../res/互通区I梁弧差-%s.dxf" % (now.strftime("%y%m%d")))
