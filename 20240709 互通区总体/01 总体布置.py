from srbpy import Align
from ezdxf.math import Vec2

D1 = Align('D1', '../Data/EI/D1')
D2 = Align('D2', '../Data/EI/D2')
D3 = Align('D3', '../Data/EI/D3')
D4 = Align('D4', '../Data/EI/D4')
M = Align('M', '../Data/EI/M')

dic = [
    (D1, 180.364),
    (D1, 213.364),
    (D1, 251.364),
    (D1, 323.364),
    (D1, 373.364),
    (D1, 406.364),
    (D1, 448.428),
    (D2, 180.364),
    (D2, 213.364),
    (D2, 251.364),
    (D2, 301.364),
    (D2, 353.364),
    (D2, 399.364),
    (D2, 435.364),
    (D2, 465.562),
    (D2, 510.562),
    (D3, 145.888),
    (D3, 184.000),
    (D3, 222.000),
    (D3, 272.000),
    (D3, 302.000),
    (D3, 332.000),
    (D4, 145.888),
    (D4, 180.888),
    (D4, 230.888),
    (D4, 280.888),
    (D4, 320.888),
    (D4, 365.888),
    (D4, 410.888),
    (M, 7.474),
    (M, 52.474),
    (M, 97.474),
    (M, 137.474),
    (M, 177.474),
    (M, 217.474),

]

st1 = D2.get_station_by_point(571279.6994, 785628.9804)
st2 = D2.get_station_by_point(571318.8471, 785620.4299)
st3 = D2.get_station_by_point(571357.8538, 785611.2571)
st4 = D2.get_station_by_point(571396.7090, 785601.4617)
d2s = [
    st1,
    st2,
    st3,
    st4,
]
for d in d2s:
    e = D2.get_elevation(d)
    print(e)
# for al, st in dic:
#     e = al.get_elevation(st)
#     g = al.get_ground_elevation(st, 0)
#     print(f"{al.name},{st:.3f},{e:.3f},{g:.3f}")

st1 = D2.get_station_by_point(571235.5898, 785638.3152)
st2 = D2.get_station_by_point(571279.6994, 785628.9804)
for st in [st1, st2]:
    e = D2.get_elevation(st)
    g = D2.get_ground_elevation(st, 0)
    print(f"D2,{st:.3f},{e:.3f},{g:.3f}")

# st = D4.get_station_by_point(571281.4846, 785637.4808)
# print(st)
# e0 = D4.get_elevation(st)
# e1 = D4.get_ground_elevation(st, 0)
# print(e0, e1)
#
