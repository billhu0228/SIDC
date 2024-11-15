import datetime

import ezdxf
from PyAngle import Angle
from ezdxf.enums import TextEntityAlignment
from ezdxf.gfxattribs import GfxAttribs
from srbpy import Align
import numpy as np
from src.beam import Beam, connect

if __name__ == '__main__':
    font_size = 0.3
    br_counter = 1
    D1 = Align('D1', '../Data/EI/D1')
    D2 = Align('D2', '../Data/EI/D2')
    D3 = Align('D3', '../Data/EI/D3')
    D4 = Align('D4', '../Data/EI/D4')
    M = Align('M', '../Data/EI/M')
    Ramps = [D1, D2, D3, D4, M]
    dxf = ['R1', 'R2', 'R3', 'R4', 'M']
    Beams = []
    Bridge = []
    for i in range(5):
        doc = ezdxf.readfile(r"..\Data\%s.dxf" % dxf[i])
        lines = doc.query('LINE')
        lines = [be for be in lines]
        lines.sort(key=lambda A: 0.5 * (A.dxf.start.x + A.dxf.end.x))
        j = 1
        for e in lines:
            pts = [e.dxf.start, e.dxf.end]
            pts.sort(key=lambda A: A.x)
            if dxf[i] in ['R1', 'R3']:
                if pts[0].x > 571177.1567:
                    raise ValueError
                elif pts[1].x > 571177.1567:
                    b = Beam(pts[1], pts[0], e.dxf.layer, M, Ramps[i], (i + 1) * 10000 + j * 100)
                else:
                    b = Beam(pts[1], pts[0], e.dxf.layer, Ramps[i], Ramps[i], (i + 1) * 10000 + j * 100)
            else:
                b = Beam(pts[1], pts[0], e.dxf.layer, Ramps[i], Ramps[i], (i + 1) * 10000 + j * 100)
            j += 1
            Beams.append(b)
    doc = ezdxf.new()
    msp = doc.modelspace()
    Bridge = [a.bridge for a in Beams]
    Bridge = np.unique(np.array(Bridge))
    for ii, br in enumerate(Bridge):
        ly = doc.layers.new(br)
        ly.color = ii + 1
        attribs = GfxAttribs(layer=br)
        girders = [g for g in connect if g[0] == br]
        if br.startswith("B"):
            BearingSyS = 0.5
            BeamH = 0.120 + 0.325 + 2.0
        else:
            raise AttributeError
            # BearingSyS = 0.65
            # BeamH = 0.120 + 2.8
        for g in girders:
            for bs in g[1:]:
                beam = [b for b in Beams if b.beam_id == bs][0]
                ed = beam.line[0]
                st = beam.line[1]
                msp.add_line(st, ed, dxfattribs=attribs)
                dirX = (ed - st).vec2.normalize().vec3
                dirU = (ed - st).normalize()
                aa = Angle.from_rad(dirU.angle_between(dirX))
                fct = 1 / aa.cos()
                dirU = dirU * fct
                dist = (ed - st).magnitude
                msp.add_text("%s-%s" % (br, bs), height=font_size, dxfattribs=attribs).set_placement(st + dist * 0.5 * dirX,
                                                                                                     align=TextEntityAlignment.MIDDLE_CENTER)
                if beam.beam_type.endswith("DE"):
                    p0 = st - 0.25 * dirU
                    msp.add_text("%s-%.3f" % ("LNR(H)-370x420x147", p0.z - BeamH),
                                 height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_CENTER)
                    br_counter += 1
                    msp.add_circle(p0, 0.25, dxfattribs=attribs)
                    p0 = ed - 0.5 * dirU
                    msp.add_text("%s-%.3f" % ("LNR(H)-370x420x147", p0.z - BeamH),
                                 height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_RIGHT)
                    br_counter += 1
                    msp.add_circle(p0, 0.25, dxfattribs=attribs)
                elif beam.beam_type.endswith("AA"):
                    p0 = st + 0.5 * dirU
                    msp.add_text("%s-%.3f" % ("LNR(H)-370x420x147", p0.z - BeamH),
                                 height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_LEFT)
                    br_counter += 1
                    msp.add_circle(p0, 0.25, dxfattribs=attribs)
                elif beam.beam_type.endswith("MM"):
                    p0 = st - 0.25 * dirU
                    msp.add_text("%s-%.3f" % ("HDR(I)-470x570x207-G1.0", p0.z - BeamH),
                                 height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_CENTER)
                    br_counter += 1
                    msp.add_circle(p0, 0.25, dxfattribs=attribs)
                elif beam.beam_type.endswith("SS"):
                    p0 = st + 0.5 * dirU
                    msp.add_text("%s-%.3f" % ("HDR(I)-370x370x177", p0.z - BeamH),
                                 height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_LEFT)
                    br_counter += 1
                    msp.add_circle(p0, 0.25, dxfattribs=attribs)
                    p0 = ed - 0.5 * dirU
                    msp.add_text("%s-%.3f" % ("HDR(I)-370x370x177", p0.z - BeamH),
                                 height=font_size).set_placement(p0, align=TextEntityAlignment.MIDDLE_RIGHT)
                    br_counter += 1
                    msp.add_circle(p0, 0.25, dxfattribs=attribs)
                else:  # 组合梁?
                    tmp = [a[1] for a in girders]
                    f = tmp.index(bs)
                    if f == 0:
                        BearingSyS = 0.5
                        p0 = st
                        msp.add_text("%i-%.3f" % (br_counter, p0.z - BeamH - BearingSyS),
                                     height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_LEFT)
                        br_counter += 1
                        msp.add_circle(p0, 0.25, dxfattribs=attribs)
                        p0 = ed
                        msp.add_text("%i-%.3f" % (br_counter, p0.z - BeamH - BearingSyS),
                                     height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_LEFT)
                        br_counter += 1
                        msp.add_circle(p0, 0.25, dxfattribs=attribs)
                    elif f == len(tmp) - 1:
                        BearingSyS = 0.5
                        p0 = ed
                        msp.add_text("%i-%.3f" % (br_counter, p0.z - BeamH - BearingSyS),
                                     height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_RIGHT)
                        br_counter += 1
                        msp.add_circle(p0, 0.25, dxfattribs=attribs)
                    else:
                        BearingSyS = 0.65
                        BeamH += 0.004
                        p0 = ed
                        msp.add_text("%.3f (%.3fm, %.3fm)" % (p0.z - BeamH - BearingSyS, BeamH, BearingSyS),
                                     height=font_size).set_placement(p0, align=TextEntityAlignment.BOTTOM_RIGHT)
                        msp.add_circle(p0, 0.25, dxfattribs=attribs)
    now = datetime.date.today()
    doc.saveas("./互通区I梁梁底高程-%s.dxf" % (now.strftime("%y%m%d")))
