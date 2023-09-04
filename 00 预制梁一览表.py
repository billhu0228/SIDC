import ezdxf
from ezdxf.math import ConstructionLine, UCS
import pandas as pd
from srbpy import Align
from src import *


def check_pier2(st0, st_dct: dict, abs_v=1.0):
    vs = list(st_dct.values())
    ks = list(st_dct.keys())
    for i, stk in enumerate(vs):
        if abs(st0 - stk) <= abs_v:
            return ks[i], ks[i + 1]
    return None


def near(al: Align, pt: Vec2, abs_v):
    st0 = al.get_station_by_point(pt.x, pt.y)
    cc0 = Vec2(al.get_coordinate(st0))
    return cc0.distance(pt) < abs_v


def check_pier(st0, stlist, abs_v=1.0):
    for i, stk in enumerate(stlist):
        if abs(st0 - stk) <= abs_v:
            return i
    return None


def LStr(ll):
    if ll <= 30:
        return '30'
    elif ll <= 35:
        return '35'
    elif ll <= 41:
        return '40'
    elif ll <= 45:
        return '45'


def getL(arr):
    return [LStr(a) for a in arr]


if __name__ == "__main__":

    doc = ezdxf.readfile("./Data/预制梁数据.dxf", encoding='gbk')

    msp = doc.modelspace()
    beams = msp.query("LINE")

    Mst = {
        "R1-7": 7.4740,
        "R1-8": 52.4740,
        "W17": 97.4740,
        "W16": 137.4740,
        "W15": 177.4740,
        "W14": 217.47187469708166,
        "W13": 262.474,
        "W12": 307.474,
        "W11": 352.474,
        "W10": 397.474,
        "W09": 442.474,
        "W08": 487.474,
        "W07": 532.474,
        "W06": 577.474,
        "W05": 622.474,
        "W04": 667.474,
        "E05": 2057.474,
        "E06": 2102.474,
        "E07": 2147.474,
        "E08": 2192.474,
        "E09": 2237.474,
        "E10": 2282.474,
        "E11": 2327.474,
        "E12": 2372.474,
        "E13": 2417.474,
        "EA": 2452.474,
    }
    sts = list(Mst.values())
    piers = list(Mst.keys())

    R1Station = {
        "SA": 180.3640,  # SA
        "R1-1": 213.3640,  # R1-1
        "R1-5": 407.7280,  # R1-5
        "R1-6": 448.4280,  # R1-6
        "R1-7": 7.4740,  # R1-7
        "R1-8": 52.4740,  # R1-8
        "W17": 97.4740,  # W17
    }

    R2Station = {
        "SA": 180.3640,  # SA
        "R2-1": 213.3640,  # R2-1
        "R2-6": 435.5618,  # R2-6
        "R2-7": 465.5618,  # R2-7
        "R2-8": 510.5618,  # R2-8
        "R2-9": 555.5618,  # R2-9
        "W17": 97.4740,  # W17
    }

    R3Station = {
        "NA": 144.3888,  # NA
        "R3-1": 184.5048,  # R3-1
    }

    R4Station = {
        "R4-4": 319.3884,  # R4-4
        "R4-5": 364.3884,  # R4-5
        "R4-6": 409.3884,  # R4-6
        "W17": 97.4740,
    }
    loc_order = {
        'E05/E06': 1, 'E06/E07': 2, 'E07/E08': 3, 'E08/E09': 4, 'E09/E10': 5, 'E10/E11': 6, 'E11/E12': 8, 'E12/E13': 9, 'E13/EA': 10,
        'W14/W13': 11, 'W13/W12': 12, 'W12/W11': 13, 'W11/W10': 14, 'W10/W09': 15, 'W09/W08': 16, 'W08/W07': 17, 'W07/W06': 18,
        'W06/W05': 19, 'W05/W04': 20,
        'W17/W16L': 21.1, 'W16/W15L': 21.2, 'W15/W14L': 21.3,
        'W17/W16R': 22.1, 'W16/W15R': 22.2, 'W15/W14R': 22.3,
        'SA/R1-1': 24, 'R1-5/R1-6': 25, 'R1-6/R1-7': 26,
        'R1-7/R1-8': 27, 'R1-8/W17': 28, 'SA/R2-1': 29, 'R2-6/R2-7': 30, 'R2-7/R2-8': 31, 'R2-8/R2-9': 32, 'R2-9/W17': 33, 'NA/R3-1': 34,
        'R4-4/R4-5': 35, 'R4-5/R4-6': 36, 'R4-6/W17': 37, }
    # ucs = UCS(origin, ux, uz)
    comb = []
    for g in beams:
        ltype = g.dxf.layer
        cc = 0.5 * (g.dxf.start + g.dxf.end)
        assert g.dxf.start.z == 0 and g.dxf.end.z == 0
        if cc.y <= 785735.5586:
            if g.dxf.start.x > g.dxf.end.x:
                st = g.dxf.end
                ed = g.dxf.start
            else:
                st = g.dxf.start
                ed = g.dxf.end
        else:
            if g.dxf.start.x > g.dxf.end.x:
                st = g.dxf.start
                ed = g.dxf.end
            else:
                st = g.dxf.end
                ed = g.dxf.start
        length = st.distance(ed)
        dirX = ed - st
        if cc.x >= M.get_coordinate(Mst['W14'])[0]:
            kk = check_pier(M.get_station_by_point(st.x, st.y), sts)
            st_pier = piers[kk]
            ed_pier = piers[kk + 1]
            side = ''
        elif cc.x >= M.get_coordinate(Mst['W17'])[0]:
            kk = check_pier(M.get_station_by_point(st.x, st.y), sts)
            st_pier = piers[kk]
            ed_pier = piers[kk + 1]
            side = 'L' if M.get_side(st.x, st.y) < 0 else "R"
        elif near(D4, Vec2(st), 5.9):
            st_pier, ed_pier = check_pier2(D4.get_station_by_point(st.x, st.y), R4Station, 5.9)
            side = ''
        elif near(D2, Vec2(st), 3.15):
            st_pier, ed_pier = check_pier2(D2.get_station_by_point(st.x, st.y), R2Station, 3.15)
            side = ''
        elif near(D1, Vec2(st), 134.5):
            if check_pier2(D1.get_station_by_point(st.x, st.y), R1Station, 13.15) is not None:
                st_pier, ed_pier = check_pier2(D1.get_station_by_point(st.x, st.y), R1Station, 13.45)
                side = ''
            else:
                st_pier, ed_pier = check_pier2(M.get_station_by_point(st.x, st.y), Mst, 13.45)
                side = ''
        elif near(D3, Vec2(st), 3.15):
            st_pier, ed_pier = check_pier2(D3.get_station_by_point(st.x, st.y), R3Station, 3.15)
            side = ''
        else:
            st_pier = ''
            ed_pier = ''
            side = ''
            print(st)
        loc = st_pier + '/' + ed_pier + side
        order = loc_order[loc]

        if loc == 34:
            span_id = st.x
        else:
            span_id = st.y
        info = [loc, ltype, Vec2(st), Vec2(ed), length, order, span_id]
        comb.append(info)
    df = pd.DataFrame(comb, columns=['Location', 'Type', "P0", 'P1', "Length", 'loc_id', 'span_id'])
    df = df.sort_values(['loc_id'])
    df = df.reset_index(drop=True)

    out = df.drop(index=df.index)
    for i, gr in df.groupby(['loc_id']):
        gr.sort_values(['span_id'], ascending=False, inplace=True)
        gr.reset_index(inplace=True, drop=True)
        gr['idx'] = gr.index
        out = out.append(gr, ignore_index=True)
    out.drop(['span_id'], axis=1, inplace=True)
    out['L'] = getL(out['Length'])

    out.to_csv('预制梁布置.csv', encoding='gbk')
