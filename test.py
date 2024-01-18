from srbpy import Align
from ezdxf.math import Vec2

D1 = Align('D1', './Data/EI/D1')
D2 = Align('D2', './Data/EI/D2')
D3 = Align('D3', './Data/EI/D3')
D4 = Align('D4', './Data/EI/D4')
M = Align('M', './Data/EI/M')


def get_surf(cl: Align, pk, dist):
    cp = cl.get_cross_slope(pk)[0] if dist < 0 else cl.get_cross_slope(pk)[1]
    return cl.get_elevation(pk) + dist * cp


if __name__ == "__main__":
    pt = Vec2(D1.get_coordinate(407.728 - 0.7))
    print("%.6f,%.6f" % (pt.x, pt.y))
    # pt = Vec2(D1.get_coordinate(213.364))
    # print(D2.get_station_by_point(pt.x, pt.y))
    # p0 = (571394.843883, 785597.37487)
#     p0 = (571437.096229, 785585.980785)
#     st = M.get_station_by_point(*p0)
#     cc = Vec2(M.get_coordinate(st))
#     e = M.get_surface_elevation(st, -0)
#     e2 = M.get_surface_elevation(st, -0.025)
#     print(st, e,e2)
#
#    st = D2.get_station_by_point(*p0)
#    cc = Vec2(D2.get_coordinate(st))
#    e = D2.get_surface_elevation(st, 4.425)
#    print(st, e)

#    st = D4.get_station_by_point(*p0)
#    cc = Vec2(D4.get_coordinate(st))
#    e = D4.get_surface_elevation(st, 7.775)
#    print(st, e)

#   print(D2.get_surface_elevation(763.840, 0))
#   print(D4.get_surface_elevation(618.117 - 0.001, 3.35))
#   print(M.get_surface_elevation(st, -0.025 - 0.475 - 0.6 - 3.35))
