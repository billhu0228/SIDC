import datetime

import ezdxf
import numpy as np
from ezdxf.enums import TextEntityAlignment
from ezdxf.gfxattribs import GfxAttribs
from srbpy import Align
from ezdxf.math import Vec2


def my_linspace(st, ed):
    ret = [st, ]
    while ret[-1] < ed:
        ret.append(ret[-1] + 30)
    return ret


def streetlight(msp, al, pk, offset):
    lay_att = GfxAttribs(layer="路灯")
    for st in pk:
        ux = Vec2(*al.get_direction(st))
        uy = ux.rotate_deg(90.0)
        cc = Vec2(*al.get_coordinate(st))
        for dy in offset:
            c0 = cc + uy * dy
            msp.add_circle(c0, 1, dxfattribs=lay_att)
            text = "%s-%.3f" % (al.name, st)
            side = "Left" if dy > 0 else "Right"
            msp.add_text(text, height=0.20, dxfattribs=lay_att).set_placement(c0, align=TextEntityAlignment.MIDDLE_CENTER)
            print(text + "-" + side)


if __name__ == '__main__':
    D1 = Align('D1', './Data/EI/D1')
    D2 = Align('D2', './Data/EI/D2')
    D3 = Align('D3', './Data/EI/D3')
    D4 = Align('D4', './Data/EI/D4')
    M = Align('M', './Data/EI/M')

    cc = Vec2(D1.get_coordinate(213.364))
    p2 = Vec2(570940.367, 785569.989)
    ss = D1.get_station_by_point(570940.367, 785569.989)
    c0 = Vec2(D1.get_coordinate(ss))
    print(c0.distance(p2))
    print(cc)
