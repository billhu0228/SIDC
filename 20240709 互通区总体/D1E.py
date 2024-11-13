from PyAngle import Angle
from srbpy import Align
from ezdxf.math import Vec2

D1 = Align('D1', '../Data/EI/D1')
D2 = Align('D2', '../Data/EI/D2')
D3 = Align('D3', '../Data/EI/D3')
D4 = Align('D4', '../Data/EI/D4')
M = Align('M', '../Data/EI/M')

p = 0
al = M
# while p < 500:
#     print("%.3f,%.3f" % (p, al.get_elevation(p)))
#     p += 1
# print("%.3f,%.3f" % (al.end_pk, al.get_elevation(al.end_pk)))


# s0 = D1.get_station_by_point(571104.2027, 785655.1518)
s0 = D4.get_station_by_point2(571096.3949, 785783.4255, 571105.0670, 785780.3402, )
A = Vec2(571096.3949, 785783.4255)
B = Vec2(571105.0670, 785780.3402)

print(s0)
cc = Vec2(D4.get_coordinate(s0))
print(cc)
p = Vec2(571100.7309, 785781.8828).distance(cc)
print(p)
ux = Vec2(D4.get_direction(s0))
ui = (B - A).normalize()
print(Angle.from_rad(ux.angle_between(ui)).to_degrees())
