import ezdxf
import pandas as pd
from ezdxf.enums import TextEntityAlignment
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.math import Vec2
from srbpy import Align
import numpy as np
from PyAngle import Angle
from src.beam import Beam, connect


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
    elif ct_type == "CP6":
        dx = [-2.25, 2.25]
        dy = [-5.34, 0, 5.34]
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
    data = pd.read_excel("./Data/互通基础参数表.xlsx", '承台参数')
    for i, row in data.iterrows():
        if not np.isnan(row['桩号']):
            st = row["桩号"]
            CL: Align = CL_dic[row['线位']]
            deg = row['基础转角']
            if not np.isnan(row['承台1']):
                result.append((row['墩台号'], row['线位'], "%7.3f" % row['桩号'], '承台1', get_piles_co(CL, st, deg, row['承台1'], row['基础类别1'])))
            if not np.isnan(row['承台2']):
                result.append((row['墩台号'], row['线位'], "%7.3f" % row['桩号'], '承台2', get_piles_co(CL, st, deg, row['承台2'], row['基础类别2'])))

    doc = ezdxf.new()
    msp = doc.modelspace()
    ly = doc.layers.new("桩基")
    ly.color = 50
    ly = doc.layers.new("承台")
    ly.color = 130
    pile_att = GfxAttribs(layer="桩基")
    ct_att = GfxAttribs(layer="承台")

    for ps in result:
        line = str(ps[0:-1])
        for p in ps[-1]:
            # print("%s: %.5f,%.5f" % (line, p.x, p.y))
            # res.append(get_piles_co(CL, st, dist, ct_type))
            msp.add_circle(p, 0.75, dxfattribs=pile_att)
            msp.add_text("(%s, pk= %.3f, E=%.3f,N%.3f)" % (ps[0], float(ps[2]), p.x, p.y),
                         height=0.1, dxfattribs=pile_att).set_placement(p, align=TextEntityAlignment.MIDDLE_CENTER)
        A, B, C, D = ps[-1][0], ps[-1][1], ps[-1][-1], ps[-1][-2]
        ux = (B - A).normalize()
        uy = (C - B).normalize()
        pts = [A + (-1.25 * ux - 1.25 * uy), B + (+1.25 * ux - 1.25 * uy), C + (+1.25 * ux + 1.25 * uy), D + (-1.25 * ux + 1.25 * uy)]
        msp.add_polyline2d(pts, close=True, dxfattribs=ct_att)
    doc.saveas("./res/互通区基础平面.dxf")
