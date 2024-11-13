import datetime
from typing import Tuple

import ezdxf
import pandas as pd
from ezdxf.enums import TextEntityAlignment
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.math import Vec2
from scipy.interpolate import interp1d
from srbpy import Align
import numpy as np
from PyAngle import Angle
from functions import get_width


def play(p0, p1, npts, cl: 'Align', info):
    fx = interp1d([p0.x, p1.x], [p0.y, p1.y])
    xs = np.linspace(p0.x, p1.x, npts)
    points = [Vec2(x, fx(x)) for x in xs]
    print(f"{info}:")
    for pp in points:
        st = cl.get_station_by_point(pp.x, pp.y)
        cc = Vec2(cl.get_coordinate(st))
        dist = cc.distance(pp)
        e1 = cl.get_surface_elevation(st, dist)
        print("%.3f,%.3f" % (st, e1))


if __name__ == '__main__':
    D1 = Align('D1', '../Data/EI/D1')
    D2 = Align('D2', '../Data/EI/D2')
    D3 = Align('D3', '../Data/EI/D3')
    D4 = Align('D4', '../Data/EI/D4')
    M = Align('Mai', '../Data/EI/M')
    play(
        Vec2(571250.7551, 785623.9668),
        Vec2(571181.6482, 785635.1516),
        71, M, "D1"
    )

    play(
        Vec2(571251.2904, 785627.2738),
        Vec2(571182.1835, 785638.4586),
        71, M, "D3"
    )

    print("D1End:", D1.get_elevation(D1.end_pk))
    print("D3End:", D3.get_elevation(D3.end_pk))
