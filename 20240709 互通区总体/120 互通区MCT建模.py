import ezdxf
from srbpy import Align
import datetime
from src.beam import Beam, connect

if __name__ == '__main__':
    D1 = Align('D1', '../Data/EI/D1')
    D2 = Align('D2', '../Data/EI/D2')
    D3 = Align('D3', '../Data/EI/D3')
    D4 = Align('D4', '../Data/EI/D4')
    M = Align('M', '../Data/EI/M')
    Ramps = [D1, D2, D3, D4, M]
    dxf = ['R1', 'R2', 'R3', 'R4', 'M']
    Beams = []
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
    now = datetime.date.today()
    with open("../res/互通区匝道-%s.mct" % (now.strftime("%y%m%d")), 'w+') as fid:
        fmct = open("../Data/template.mct", 'r')
        lines = fmct.readlines()
        fmct.close()
        nlist = []
        elist = []
        hdr = []
        for line in lines:
            fid.write(line)
        for b in Beams:
            b.make_nodes()
            # b.make_nodes_no_use()
            nlist += b.nlist
            elist += b.elist
            hdr += b.hdr
        fid.write("*NODE\n")
        for n in nlist:
            fid.write("%i,%.6f,%.6f,%.6f\n" % (n[0], n[1], n[2], n[3]))
        fid.write("*Element\n")
        for e in elist:
            fid.write(" %i,BEAM,%i,%i,%i,%i,0,0\n" % (e[0], e[1], e[2], e[3], e[4]))
        fid.write("*NODE\n")
        for n in hdr:
            fid.write("%i,%.6f,%.6f,%.6f\n" % (n[0], n[1], n[2], n[3]))
        fid.write("*NL-LINK\n")
        nl = 1
        for n in hdr:
            fid.write(" %i, %i, %i, HDR720, , 0, 0, \n" % (nl, n[0], n[4]))
            nl += 1
        fid.write("*CONSTRAINT\n")
        for n in hdr:
            fid.write("%i, 111111,\n" % (n[0]))
