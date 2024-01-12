from srbpy import Align
from ezdxf.math import Vec2

D1 = Align('D1', './Data/EI/D1')
D2 = Align('D2', './Data/EI/D2')
D3 = Align('D3', './Data/EI/D3')
D4 = Align('D4', './Data/EI/D4')
M = Align('M', './Data/EI/M')

Mst = {
    "# R1-7": 7.4740,
    "# R1-8": 52.4740,
    "# W17": 97.4740,
    " # W16": 137.4740,
    " # W15": 177.4740,
    " # W14": 217.47187469708166,
    "# W13": 262.474,
    "# W12": 307.474,
    "# W11": 352.474,
    "# W10": 397.474,
    "# W09": 442.474,
    "# W08": 487.474,
    "# W07": 532.474,
    "# W06": 577.474,
    "# W05": 622.474,
    "# W04": 667.474,
    " # E05": 2057.474,
    " # E06": 2102.474,
    " # E07": 2147.474,
    " # E08": 2192.474,
    " # E09": 2237.474,
    " # E10": 2282.474,
    " # E11": 2327.474,
    " # E12": 2372.474,
    " # E13": 2417.474,
    " # EA": 2452.474,
}

R1Station = {
    "# SA": 180.3640,
    "# R1-1": 213.3640,
    "# R1-2": 251.364,
    "# R1-3": 322.364,
    "# R1-4": 367.364,
    "# R1-5": 407.7280,
    "# R1-6": 448.4280,
    "# R1-7": 7.4740,
    "# R1-8": 52.4740,
    "# W17": 97.4740,
}

R2Station = {
    "# SA": 180.3640,
    "# R2-1": 213.3640,
    "# R2-3": 301.364,
    "# R2-4": 352.562,
    "# R2-5": 395.562,
    "# R2-6": 435.5618,
    "# R2-7": 465.5618,
    "# R2-8": 510.5618,
    "# R2-9": 555.5618,
}
R3Station = {
    "# NA": 144.3888,
    "# R3-1": 184.505,
    "# R3-2": 219.505,
    "# R3-3": 269.505,
    "# R3-4": 302.505,
    "# R3-5": 332.505,

}
R4Station = {
    "# R4-1": 177.388,
    "# R4-2": 234.388,
    "# R4-3": 279.388,
    "# R4-4": 319.3884,
    "# R4-5": 364.3884,
    "# R4-6": 409.3884,
}

print("---M---")
for k in Mst.keys():
    st = Mst[k]
    print("%s: %.3f, %.3f" % (k, st, M.get_ground_elevation(st, 0)))

print("---R1---")
for k in R1Station.keys():
    st = R1Station[k]
    print("%s: %.3f, %.3f" % (k, st, D1.get_ground_elevation(st, 0)))

print("----R2-----")
for k in R2Station.keys():
    st = R2Station[k]
    print("%s: %.3f, %.3f" % (k, st, D2.get_ground_elevation(st, 0)))

print("----R3-----")
for k in R3Station.keys():
    st = R3Station[k]
    print("%s: %.3f, %.3f" % (k, st, D3.get_ground_elevation(st, 0)))

print("----R4-----")
for k in R4Station.keys():
    st = R4Station[k]
    print("%s: %.3f, %.3f" % (k, st, D4.get_ground_elevation(st, 0)))
