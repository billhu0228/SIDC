from sectionproperties.analysis import Section

from src.Nu2000Sect import comp_sections, un2k, C65

if __name__ == '__main__':
    i1, s1, c1 = comp_sections(1400, 1550)
    i2, s2, c2 = comp_sections(1400, 1550, True)
    # c1.plot_mesh()
    # c2.plot_mesh()
    sections = [i1, c1, i2, c2]
    for s in sections:
        a = s.get_area() * 1e-6
        i = s.get_eic(e_ref=C65)[0] * 1e-12
        bds = s.geometry.geom.bounds
        cc = s.get_c()
        czp = (bds[3] - cc[1]) * 1e-3
        czg = (0 - cc[1]) * 1e-3
        czm = (cc[1] - bds[1]) * 1e-3
        print("%.3f\t%.3f\t%.3f\t%.3f\t%.3f" % (a, i, czm, czg, czp))
