from srbpy import Align
from ezdxf.math import Vec2

D1 = Align('D1', './Data/EI/D1')
D2 = Align('D2', './Data/EI/D2')
D3 = Align('D3', './Data/EI/D3')
D4 = Align('D4', './Data/EI/D4')
M = Align('M', './Data/EI/M')

print(D1.get_elevation(300))
print(M.get_coordinate(97.4740, ))

p = (571320.0385342, 785626.8178289)
e1 = M.get_surface_elevation(M.get_station_by_point(*p), 10.9436)
e2 = D4.get_surface_elevation(D4.get_station_by_point(*p), 0.0930209)
print(e1, e2)

Mst = [
    7.4740,  # R1-7
    52.4740,  # R1-8
    97.4740,  # W17
    137.4740,  # W16
    177.4740,  # W15
    217.47187469708166,  # W14
    262.474,  # W13
    307.474,  # W12
    352.474,  # W11
    397.474,  # W10
    442.474,  # W09
    487.474,  # W08
    532.474,  # W07
    577.474,  # W06
    622.474,  # W05
    667.474,  # W04
    2057.474,  # E05
    2102.474,  # E06
    2147.474,  # E07
    2192.474,  # E08
    2237.474,  # E09
    2282.474,  # E10
    2327.474,  # E11
    2372.474,  # E12
    2417.474,  # E13
    2452.474,  # EA
]

R1Station = [
    180.3640,  # SA
    213.3640,  # R1-1
    322.364,  # R1-3
    367.364,  # R1-4
    407.7280,  # R1-5
    448.4280,  # R1-6
    7.4740,  # R1-7
    52.4740,  # R1-8
    97.4740,  # W17
]

R2Station = [
    180.3640,  # SA
    213.3640,  # R2-1
    435.5618,  # R2-6
    465.5618,  # R2-7
    510.5618,  # R2-8
    555.5618,  # R2-9
]
R3Station = [
    144.3888,  # NA
    184.5048,  # R3-1
]

R4Station = [
    319.3884,  # R4-4
    364.3884,  # R4-5
    409.3884,  # R4-6
]

# ST14 = M.get_station_by_point(571395.5844493, 785597.1557535)
# print(ST14)
print("---M---")
for st in Mst:
    cc = Vec2(M.get_coordinate(st))
    ddir = Vec2(M.get_direction(st))
    ydir = ddir.rotate_deg(90)
    left = cc + ydir * 10
    right = cc - ydir * 10
    # print("%.8f,%.8f" % (left[0], left[1]))
    # print("%.8f,%.8f" % (cc[0], cc[1]))
    # print("%.8f,%.8f" % (right[0], right[1]))
    # print(M.get_ground_elevation(st, 0))
    print("%.3f纵坡: %.3f" % (st, M.get_slope(st)))
#     # print("%.6f,%.6f" % (ddir[0], ddir[1]))
print("---R1---")
for st in R1Station:
    cc = Vec2(D1.get_coordinate(st))
    ddir = Vec2(D1.get_direction(st))
    ydir = ddir.rotate_deg(90)
    left = cc + ydir * 10
    right = cc - ydir * 10
    # print("%.8f,%.8f" % (left[0], left[1]))
    # print("%.8f,%.8f" % (cc[0], cc[1]))
    # print("%.8f,%.8f" % (right[0], right[1]))
    print("%.3f纵坡: %.3f" % (st, D1.get_slope(st)))
print("----R2-----")
for st in R2Station:
    cc = Vec2(D2.get_coordinate(st))
    ddir = Vec2(D2.get_direction(st))
    ydir = ddir.rotate_deg(90)
    left = cc + ydir * 10
    right = cc - ydir * 10
    # print("%.8f,%.8f" % (left[0], left[1]))
    # print("%.8f,%.8f" % (cc[0], cc[1]))
    # print("%.8f,%.8f" % (right[0], right[1]))
    print("%.3f纵坡: %.3f" % (st, D2.get_slope(st)))
print("----R3-----")
for st in R3Station:
    cc = Vec2(D3.get_coordinate(st))
    ddir = Vec2(D3.get_direction(st))
    ydir = ddir.rotate_deg(90)
    left = cc + ydir * 10
    right = cc - ydir * 10
    # print("%.8f,%.8f" % (left[0], left[1]))
    # print("%.8f,%.8f" % (cc[0], cc[1]))
    # print("%.8f,%.8f" % (right[0], right[1]))
    print("%.3f纵坡: %.3f" % (st, D3.get_slope(st)))
print("----R4-----")
for st in R4Station:
    cc = Vec2(D4.get_coordinate(st))
    ddir = Vec2(D4.get_direction(st))
    ydir = ddir.rotate_deg(90)
    left = cc + ydir * 10
    right = cc - ydir * 10
    # print("%.8f,%.8f" % (left[0], left[1]))
    # print("%.8f,%.8f" % (cc[0], cc[1]))
    # print("%.8f,%.8f" % (right[0], right[1]))
    print("%.3f纵坡: %.3f" % (st, D4.get_slope(st)))
