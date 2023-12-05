import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.gfxattribs import GfxAttribs
from srbpy import Align
import numpy as np
from src.beam import Beam, connect

if __name__ == '__main__':

    D1 = Align('D1', './Data/EI/D1')
    D2 = Align('D2', './Data/EI/D2')
    D3 = Align('D3', './Data/EI/D3')
    D4 = Align('D4', './Data/EI/D4')
    M = Align('M', './Data/EI/M')
    Ramps = [D1, D2, D3, D4, M]
    dxf = ['R1', 'R2', 'R3', 'R4', 'M']
    Beams = []
    Bridge = []
    for i in range(5):
        doc = ezdxf.readfile(r".\Data\%s.dxf" % dxf[i])
        j = 1
        for e in doc.modelspace():
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
    BearingSyS = 0.5
    BeamH = 0.120 + 0.325 + 2.0
    for ii, br in enumerate(Bridge):
        ly = doc.layers.new(br)
        ly.color = ii + 1
        attribs = GfxAttribs(layer=br)
        girders = [g for g in connect if g[0] == br]
        for g in girders:
            last_ed = None
            for bs in g[1:]:
                beam = [b for b in Beams if b.beam_id == bs][0]
                st = beam.line[0]
                ed = beam.line[1]
                msp.add_line(st, ed, dxfattribs=attribs)
                if beam.beam_type.endswith("DE"):
                    dirX = (ed - st).normalize()
                    p0 = st + 0.5 * dirX
                    msp.add_text("%.3f" % (p0.z - BeamH - BearingSyS), height=0.5).set_placement(p0, align=TextEntityAlignment.MIDDLE_RIGHT)
                    last_ed = ed
                elif beam.beam_type.endswith("AA"):
                    dirX = (st - last_ed).normalize()
                    dist = (st - last_ed).magnitude
                    p0 = last_ed + 0.5 * dist * dirX
                    msp.add_text("%.3f" % (p0.z - BeamH - BearingSyS), height=0.5).set_placement(p0, align=TextEntityAlignment.MIDDLE_LEFT)
                    last_ed = ed
                    dirX = (ed - st).normalize()
                    p0 = ed - 0.5 * dirX
                    msp.add_text("%.3f" % (p0.z - BeamH - BearingSyS), height=0.5).set_placement(p0, align=TextEntityAlignment.MIDDLE_LEFT)
                elif beam.beam_type.endswith("MM"):
                    dirX = (st - last_ed).normalize()
                    dist = (st - last_ed).magnitude
                    p0 = last_ed + 0.5 * dist * dirX
                    msp.add_text("%.3f" % (p0.z - BeamH - BearingSyS), height=0.5).set_placement(p0, align=TextEntityAlignment.MIDDLE_LEFT)
                    last_ed = ed
                else:
                    dirX = (ed - st).normalize()
                    p0 = st + 0.5 * dirX
                    msp.add_text("%.3f" % (p0.z - BeamH - BearingSyS), height=0.5).set_placement(p0, align=TextEntityAlignment.MIDDLE_RIGHT)
                    p0 = ed - 0.5 * dirX
                    msp.add_text("%.3f" % (p0.z - BeamH - BearingSyS), height=0.5).set_placement(p0, align=TextEntityAlignment.MIDDLE_LEFT)
    doc.saveas("./res/互通区预制梁垫石底标高（系统总高H=0.5m）.dxf")
