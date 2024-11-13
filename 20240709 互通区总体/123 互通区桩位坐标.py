import datetime
from typing import Tuple

import ezdxf
import pandas as pd
from ezdxf.enums import TextEntityAlignment
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.math import Vec2
from srbpy import Align
import numpy as np
from PyAngle import Angle
from functions import get_width


def get_cb_co(M: Align, station: float, degree, offset_xy: Tuple[float, float], wl, wr, wt):
    cc = Vec2(M.get_coordinate(station))
    ux = Vec2(M.get_direction(station))
    uy = ux.rotate(Angle.from_degrees(degree).to_rad())
    ux = uy.rotate(Angle.from_degrees(-90.0).to_rad())
    p0 = cc + ux * offset_xy[0] + uy * offset_xy[1]
    res = []
    if np.isnan(wl):
        debug = 0
    res.append(
        [
            p0 + ((-0.5 * wt) * ux + (+ wl) * uy),
            p0 + ((+0.5 * wt) * ux + (+ wl) * uy),
            p0 + ((+0.5 * wt) * ux + (- wr) * uy),
            p0 + ((-0.5 * wt) * ux + (- wr) * uy),

        ]
    )
    return res


def get_pier_co(M: Align, station: float, degree, offset_xy: Tuple[float, float], pi_type: 'str'):
    cc = Vec2(M.get_coordinate(station))
    ux = Vec2(M.get_direction(station))
    uy = ux.rotate(Angle.from_degrees(degree).to_rad())
    ux = uy.rotate(Angle.from_degrees(-90.0).to_rad())
    p0 = cc + ux * offset_xy[0] + uy * offset_xy[1]
    dx = []
    dy = []
    res = []
    if pi_type == "PI0":
        w = 2.5
        h = 1.6
        cha = 0.25
    elif pi_type == "PI1":
        w = 2.5
        h = 2.0
        cha = 0.25
    elif pi_type == "PI3":
        w = 3.0
        h = 2.3
        cha = 0.25
    else:
        raise NotImplementedError
    res.append(
        [
            p0 + ((-0.5 * h + cha) * ux + (- 0.5 * w) * uy), p0 + ((-0.5 * h) * ux + (- 0.5 * w + cha) * uy),
            p0 + ((-0.5 * h) * ux + (+ 0.5 * w - cha) * uy), p0 + ((-0.5 * h + cha) * ux + (+ 0.5 * w) * uy),
            p0 + ((+0.5 * h - cha) * ux + (+ 0.5 * w) * uy), p0 + ((+0.5 * h) * ux + (+ 0.5 * w - cha) * uy),
            p0 + ((+0.5 * h) * ux + (- 0.5 * w + cha) * uy), p0 + ((+0.5 * h - cha) * ux + (- 0.5 * w) * uy),
        ]
    )
    return res


def get_piles_co(M: Align, station: float, degree, offset_xy: Tuple[float, float], ct_type: 'str'):
    cc = Vec2(M.get_coordinate(station))
    # deg = row['基础转角']
    ux = Vec2(M.get_direction(station))
    uy = ux.rotate(Angle.from_degrees(degree).to_rad())
    ux = uy.rotate(Angle.from_degrees(-90.0).to_rad())
    p0 = cc + ux * offset_xy[0] + uy * offset_xy[1]
    dx = []
    dy = []
    res = []
    rm = []
    if ct_type == "CP1":
        dx = [-2.25, 2.25]
        dy = [-2.25, 2.25]
    elif ct_type == "CP1a":
        dx = [-3.2, 0, 3.2]
        dy = [-3.2, 0, 3.2]
        rm = [1, 3, 5, 7]
    elif ct_type == "CP4":
        dx = [-2.25, 2.25]
        dy = [-6.75, -2.25, 2.25, 6.75]
    elif ct_type == "CP5":
        dx = [-2.25, 2.25]
        dy = [-4.5, 0, 4.5]
    elif ct_type == "CP9":
        dx = [-6, 0, 6]
        dy = [-6, 0, 6]
    elif ct_type == "CP10":
        dx = [-2.25, 2.25]
        dy = [-9, -4.5, 0, 4.5, 9]
    elif ct_type == "CP12":
        dx = [-6, 0, 6]
        dy = [-9, -3, 3, 9]
    i = 0
    for yy in dy:
        for xx in dx:
            point = p0 + ux * xx + uy * yy
            if i not in rm:
                res.append(point)
            i += 1
    return res


def foundation():
    result = []
    data = pd.read_excel("../Data/互通基础参数表-R03.xlsx", '承台参数')
    for i, row in data.iterrows():
        st = row["桩号"]
        CL: Align = CL_dic[row['线位']]
        if isinstance(row['基础类别1'], str):
            deg = row['承台1转角']
            if pd.isna(row['left']) or pd.isna(row['right']):
                offset = [float(d) for d in row['承台1偏位'].split(',')]
            else:
                wl = get_width('边线.dxf', CL, st, True, row['left'])
                wr = get_width('边线.dxf', CL, st, False, row['right'])
                if wr is None:  # 都在左侧
                    wr = get_width('边线.dxf', CL, st, True, row['right'])
                    offset = (0, 0.5 * (wl + wr))
                else:
                    assert isinstance(wr, float) and isinstance(wl, float)
                    offset = (0, 0.5 * (wl - wr))
            result.append(
                (row['墩台号'], row['线位'], "%7.3f" % row['桩号'], '承台1', row['基础类别1'],
                 get_piles_co(CL, st, deg, offset, row['基础类别1'])))
            if isinstance(row['基础类别2'], str):
                deg = row['承台2转角']
                if pd.isna(row['left2']) or pd.isna(row['right2']):
                    offset = [float(d) for d in row['承台2偏位'].split(',')]
                else:
                    wl = get_width('边线.dxf', CL, st, True, row['left2'])
                    wr = get_width('边线.dxf', CL, st, False, row['right2'])
                    if wl is None:  # 都在设计线右侧
                        wl = get_width('边线.dxf', CL, st, False, row['left2'])
                        offset = (0, -0.5 * (wl + wr))
                    else:
                        assert isinstance(wr, float) and isinstance(wl, float)
                        offset = (0, 0.5 * (wl - wr))
                result.append(
                    (row['墩台号'], row['线位'], "%7.3f" % row['桩号'], '承台2', row['基础类别2'],
                     get_piles_co(CL, st, deg, offset, row['基础类别2'])))

    doc = ezdxf.new()
    msp = doc.modelspace()
    ly = doc.layers.new("桩基")
    ly.color = 50
    ly = doc.layers.new("承台")
    ly.color = 130
    pile_att = GfxAttribs(layer="桩基")
    ct_att = GfxAttribs(layer="承台")

    for ps in result:
        if pd.isna(ps[4]):
            continue
        line = str(ps[0:-1])
        for p in ps[-1]:
            # print("%s: %.5f,%.5f" % (line, p.x, p.y))
            # res.append(get_piles_co(CL, st, dist, ct_type))
            msp.add_circle(p, 0.75, dxfattribs=pile_att)
            text = "(%s, pk= %.3f, E=%.3f,N%.3f)" % (ps[0], float(ps[2]), p.x, p.y)
            msp.add_text(text, height=0.1, dxfattribs=pile_att).set_placement(p, align=TextEntityAlignment.MIDDLE_CENTER)
            print(text)
        piles = ps[-1]
        if len(piles) in [9, 12]:
            A, B, C, D = piles[0], piles[2], piles[-1], piles[-3]
        else:
            A, B, C, D = ps[-1][0], ps[-1][1], ps[-1][-1], ps[-1][-2]
        ux = (B - A).normalize()
        uy = (C - B).normalize()
        pts = [A + (-1.25 * ux - 1.25 * uy), B + (+1.25 * ux - 1.25 * uy), C + (+1.25 * ux + 1.25 * uy), D + (-1.25 * ux + 1.25 * uy)]
        msp.add_polyline2d(pts, close=True, dxfattribs=ct_att)

    now = datetime.date.today()
    doc.saveas("../res/互通区基础平面-%s.dxf" % (now.strftime("%y%m%d")))


def pier():
    result = []
    data = pd.read_excel("../Data/互通基础参数表-R03.xlsx", '墩柱参数')
    for i, row in data.iterrows():
        st = row["桩号"]
        if row['墩台号'] == "W16":
            print(row['墩台号'])
        CL: Align = CL_dic[row['线位']]
        if isinstance(row['墩柱类别1'], str):
            deg = row['墩柱1转角']
            if pd.isna(row['left']) or pd.isna(row['right']):
                offset = [float(d) for d in row['墩柱1偏位'].split(',')]
            else:
                wl = get_width('边线.dxf', CL, st, True, row['left'])
                wr = get_width('边线.dxf', CL, st, False, row['right'])
                if wr is None:  # 都在左侧
                    wr = get_width('边线.dxf', CL, st, True, row['right'])
                    offset = (0, 0.5 * (wl + wr))
                else:
                    assert isinstance(wr, float) and isinstance(wl, float)
                    offset = (0, 0.5 * (wl - wr))
            result.append(
                (row['墩台号'], row['线位'], "%7.3f" % row['桩号'], '承台1', row['墩柱类别1'],
                 get_pier_co(CL, st, deg, offset, row['墩柱类别1'])))
            if isinstance(row['墩柱类别2'], str):
                deg = row['墩柱2转角']
                if pd.isna(row['left2']) or pd.isna(row['right2']):
                    offset = [float(d) for d in row['墩柱2偏位'].split(',')]
                else:
                    wl = get_width('边线.dxf', CL, st, True, row['left2'])
                    wr = get_width('边线.dxf', CL, st, False, row['right2'])
                    if wl is None:  # 都在设计线右侧
                        wl = get_width('边线.dxf', CL, st, False, row['left2'])
                        offset = (0, -0.5 * (wl + wr))
                    else:
                        assert isinstance(wr, float) and isinstance(wl, float)
                        offset = (0, 0.5 * (wl - wr))
                result.append(
                    (row['墩台号'], row['线位'], "%7.3f" % row['桩号'], '承台2', row['墩柱类别2'],
                     get_pier_co(CL, st, deg, offset, row['墩柱类别2'])))
    doc = ezdxf.new()
    msp = doc.modelspace()
    ly = doc.layers.new("墩柱")
    ly.color = 80
    ly = doc.layers.new("盖梁")
    ly.color = 240
    pier_att = GfxAttribs(layer="墩柱")
    cb_att = GfxAttribs(layer="盖梁")
    for ps in result:
        if pd.isna(ps[4]):
            continue
        if len(ps[-1]) == 0:
            continue
        else:
            msp.add_polyline2d(ps[-1][0], close=True, dxfattribs=pier_att)
    now = datetime.date.today()
    doc.saveas("../res/互通区墩柱平面-%s.dxf" % (now.strftime("%y%m%d")))


def crossbeam():
    result = []
    data = pd.read_excel("../Data/互通基础参数表-R03.xlsx", '盖梁参数')
    for i, row in data.iterrows():
        st = row["桩号"]
        if row['墩台号'] == "R2-2":
            print(row['墩台号'])
        CL: Align = CL_dic[row['线位']]
        if isinstance(row['盖梁1'], str):
            deg = row['盖梁1转角']
            cb_wl = row['盖梁1wl']
            cb_wr = row['盖梁1wr']
            cb_wt = row['盖梁1wt']
            if pd.isna(row['left']) or pd.isna(row['right']):
                offset = [float(d) for d in row['盖梁1偏位'].split(',')]
            else:
                wl = get_width('边线.dxf', CL, st, True, row['left'])
                wr = get_width('边线.dxf', CL, st, False, row['right'])
                if wr is None:  # 都在左侧
                    wr = get_width('边线.dxf', CL, st, True, row['right'])
                    offset = (0, 0.5 * (wl + wr))
                else:
                    assert isinstance(wr, float) and isinstance(wl, float)
                    offset = (0, 0.5 * (wl - wr))
            result.append(
                (row['墩台号'], row['线位'], "%7.3f" % row['桩号'], '盖梁1',
                 get_cb_co(CL, st, deg, offset, cb_wl, cb_wr, cb_wt)))
        if isinstance(row['盖梁2'], str):
            deg = row['盖梁2转角']
            cb_wl = row['盖梁2wl']
            cb_wr = row['盖梁2wr']
            cb_wt = row['盖梁2wt']
            if pd.isna(row['left']) or pd.isna(row['right']):
                offset = [float(d) for d in row['盖梁2偏位'].split(',')]
            else:
                wl = get_width('边线.dxf', CL, st, True, row['left2'])
                wr = get_width('边线.dxf', CL, st, False, row['right2'])
                if wl is None:  # 都在设计线右侧
                    wl = get_width('边线.dxf', CL, st, False, row['left2'])
                    offset = (0, -0.5 * (wl + wr))
                else:
                    assert isinstance(wr, float) and isinstance(wl, float)
                    offset = (0, 0.5 * (wl - wr))
            result.append(
                (row['墩台号'], row['线位'], "%7.3f" % row['桩号'], '盖梁2',
                 get_cb_co(CL, st, deg, offset, cb_wl, cb_wr, cb_wt)))
    doc = ezdxf.new()
    msp = doc.modelspace()
    ly = doc.layers.new("盖梁")
    ly.color = 240
    cb_att = GfxAttribs(layer="盖梁")
    for ps in result:
        if len(ps[-1]) == 0:
            continue
        else:
            msp.add_polyline2d(ps[-1][0], close=True, dxfattribs=cb_att)
    now = datetime.date.today()
    doc.saveas("../res/互通区盖梁平面-%s.dxf" % (now.strftime("%y%m%d")))


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
    foundation()
    # pier()
    # crossbeam()
