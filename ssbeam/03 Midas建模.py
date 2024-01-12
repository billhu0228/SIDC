from ezdxf.math import Vec3

from src.ssbeam import SSBeam

if __name__ == '__main__':
    b1 = SSBeam(Vec3(0, -1.4, 0), Vec3(40, -1.4, 0), 10000)
    with open("../res/简支梁.mct", 'w+') as fid:
        fmct = open("../Data/template.mct", 'r')
        lines = fmct.readlines()
        fmct.close()
        nlist = []
        elist = []
        hdr = []
        for line in lines:
            fid.write(line)
        for b in [b1, ]:
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
