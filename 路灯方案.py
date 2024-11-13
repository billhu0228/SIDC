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

    doc = ezdxf.new()
    msp = doc.modelspace()
    ly1 = doc.layers.new("路灯")
    ly1.color = 210

    streetlight(msp, M, my_linspace(113.371, 2452.474), [+9.950, ])
    streetlight(msp, M, my_linspace(23.371, 2452.474), [-9.950, ])
    streetlight(msp, D1, my_linspace(0, 480), [-2.15])
    streetlight(msp, D2, my_linspace(0, 600), [+2.15])
    streetlight(msp, D3, my_linspace(0, 330), [-2.15])
    streetlight(msp, D4, my_linspace(0, 450), [+2.15])

    now = datetime.date.today()
    doc.saveas("./res/全线路灯布置总图-%s.dxf" % (now.strftime("%y%m%d")))
