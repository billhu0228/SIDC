import numpy as np
from sectionproperties.analysis import Section
from sectionproperties.pre import pre, geometry, Material
from sectionproperties.pre.library import i_girder_section
from sectionproperties.pre.library import rectangular_section
from shapely import Polygon

C65 = Material(
    name="C65",
    elastic_modulus=1,
    poissons_ratio=0.2,
    density=2.4e-6,
    yield_strength=65,
    color="lightgrey",
)
C50 = Material(
    name="C50",
    elastic_modulus=0.8770580193070293,
    poissons_ratio=0.2,
    density=2.4e-6,
    yield_strength=50,
    color="burlywood",
)


def un2ke(girder_type: int, material: pre.Material = pre.DEFAULT_MATERIAL, ) -> geometry.Geometry:
    if girder_type < 1 or girder_type > 4:
        msg = "I Girder Type must be between 1 and 4"
        raise ValueError(msg)
    points: list[tuple[float, float]] = []
    points.append((630.0000, -19.1591))
    points.append((629.3195, -27.3487))
    points.append((627.3052, -35.3478))
    points.append((624.0034, -42.9005))
    points.append((619.5102, -49.8001))
    points.append((613.9485, -55.8664))
    points.append((607.4641, -60.9404))
    points.append((600.2259, -64.8841))
    points.append((592.4313, -67.5838))
    points.append((584.3315, -68.9712))
    points.append((505.0000, -75.8696))
    points.append((505.0000, -1980.0000))
    points.append((485.0000, -2000.0000))
    points.append((-485.0000, -2000.0000))
    points.append((-505.0000, -1980.0000))
    points.append((-505.0000, -75.8696))
    points.append((-584.3315, -68.9712))
    points.append((-592.4313, -67.5838))
    points.append((-600.2259, -64.8841))
    points.append((-607.4641, -60.9404))
    points.append((-613.9485, -55.8664))
    points.append((-619.5102, -49.8001))
    points.append((-624.0034, -42.9005))
    points.append((-627.3052, -35.3478))
    points.append((-629.3195, -27.3487))
    points.append((-630.0000, -19.1591))
    points.append((-630.0000, 0.0000))
    points.append((630.0000, 0.0000))
    return geometry.Geometry(geom=Polygon(points), material=material)


def un2k(girder_type: int, material: pre.Material = pre.DEFAULT_MATERIAL, ) -> geometry.Geometry:
    if girder_type < 1 or girder_type > 4:
        msg = "I Girder Type must be between 1 and 4"
        raise ValueError(msg)
    # initialise points variable
    points: list[tuple[float, float]] = []
    # Origin at centre top; clockwise from top right corner
    points.append((485.0000, -2000.0000))
    points.append((-485.0000, -2000.0000))
    points.append((-505.0000, -1980.0000))
    points.append((-505.0000, -1900.2500))
    points.append((-504.2300, -1891.5000))
    points.append((-501.9500, -1883.0600))
    points.append((-498.2300, -1875.1300))
    points.append((-493.1800, -1867.9000))
    points.append((-486.9600, -1861.8000))
    points.append((-479.7600, -1856.8100))
    points.append((-471.7900, -1853.1000))
    points.append((-245.3100, -1772.3710))
    points.append((-213.4600, -1757.7510))
    points.append((-184.6500, -1737.7900))
    points.append((-159.7600, -1713.1170))
    points.append((-139.5700, -1684.4740))
    points.append((-124.6800, -1652.7400))
    points.append((-115.5700, -1618.9070))
    points.append((-112.5000, -1583.9960))
    points.append((-112.5000, -293.4000))
    points.append((-115.9300, -256.4700))
    points.append((-126.1000, -220.8500))
    points.append((-142.6800, -187.8000))
    points.append((-165.0800, -158.2100))
    points.append((-192.5400, -133.3300))
    points.append((-224.1100, -114.0000))
    points.append((-258.7200, -100.7300))
    points.append((-295.1700, -94.1200))
    points.append((-584.3300, -69.0000))
    points.append((-593.4400, -67.3200))
    points.append((-602.0900, -64.0100))
    points.append((-609.9900, -59.2000))
    points.append((-616.8500, -52.9500))
    points.append((-622.4500, -45.5700))
    points.append((-626.5900, -37.3000))
    points.append((-629.1400, -28.3800))
    points.append((-630.0000, -19.1600))
    points.append((-630.0000, 0.0000))
    points.append((630.0000, 0.0000))
    points.append((630.0000, -19.1600))
    points.append((629.1400, -28.3800))
    points.append((626.5900, -37.3000))
    points.append((622.4500, -45.5700))
    points.append((616.8500, -52.9500))
    points.append((609.9900, -59.2000))
    points.append((602.0900, -64.0100))
    points.append((593.4400, -67.3200))
    points.append((584.3300, -69.0000))
    points.append((295.1700, -94.1200))
    points.append((258.7200, -100.7300))
    points.append((224.1100, -114.0000))
    points.append((192.5400, -133.3300))
    points.append((165.0800, -158.2100))
    points.append((142.6800, -187.8000))
    points.append((126.1000, -220.8500))
    points.append((115.9300, -256.4700))
    points.append((112.5000, -293.4000))
    points.append((112.5000, -1583.9960))
    points.append((115.5700, -1618.9070))
    points.append((124.6800, -1652.7400))
    points.append((139.5700, -1684.4740))
    points.append((159.7600, -1713.1170))
    points.append((184.6500, -1737.7900))
    points.append((213.4600, -1757.7510))
    points.append((245.3100, -1772.3710))
    points.append((471.7900, -1853.1000))
    points.append((479.7600, -1856.8100))
    points.append((486.9600, -1861.8000))
    points.append((493.1800, -1867.9000))
    points.append((498.2300, -1875.1300))
    points.append((501.9500, -1883.0600))
    points.append((504.2300, -1891.5000))
    points.append((505.0000, -1900.2500))
    points.append((505.0000, -1980.0000))
    return geometry.Geometry(geom=Polygon(points), material=material)


def Part2MCT(fid, part1: Section, part2: Section, comp: Section, Cx, bot_width, E=1.0, poly_str=""):
    fid.write("   PART=%i\n" % 1)
    area = part1.get_area()
    EA = E * part1.get_area()
    eas = part1.get_eas()
    J = part1.get_ej()
    EI = part1.get_eic()
    fid.write("       %.0f, %.0f, %.0f, %.0f, %.5e, %.5e,%.5e\n" % (area, EA, eas[0], eas[1], J, EI[0], EI[1]))
    bds = part1.geometry.geom.bounds
    cc = part1.get_c()
    cyp_p1 = bds[2] - cc[0]
    cym_p1 = cc[0] - bds[0]
    czp_p1 = bds[3] - cc[1]
    czm_p1 = cc[1] - bds[1]
    peri = part1.get_perimeter()
    fid.write("       %.0f, %.0f, %.0f, %.0f, 0, 0, %.0f, 0, %.0f, %.0f\n" % (cyp_p1, cym_p1, czp_p1, czm_p1, peri, Cx, czm_p1))
    fid.write("       %.0f, %.0f, %.0f, %.0f, " % (-cym_p1, cyp_p1, 0.5 * bot_width, -0.5 * bot_width))
    fid.write(" %.0f, %.0f, %.0f, %.0f\n" % (czp_p1, czp_p1, -czm_p1, -czm_p1))
    fid.write("       %.0f, %.0f, %.0f, %.0f, %.5e, %.5e,%.5e\n" % (area, EA, eas[0], eas[1], J, EI[0], EI[1]))
    fid.write("       %.0f, %.0f, %.0f, %.0f, 0, 0, %.0f, 0, %.0f, %.0f\n" % (cyp_p1, cym_p1, czp_p1, czm_p1, peri, Cx, czm_p1))
    fid.write("       %.0f, %.0f, %.0f, %.0f, " % (-cym_p1, cyp_p1, 0.5 * bot_width, -0.5 * bot_width))
    fid.write(" %.0f, %.0f, %.0f, %.0f\n" % (czp_p1, czp_p1, -czm_p1, -czm_p1))
    fid.write("       1, YES, YES, 1.0, 0.2\n")
    fid.write("       OPOLY=%s" % poly_str)
    for k, pt in enumerate(part1.geometry.points):
        fid.write("%.6f, %.6f" % (pt[0], pt[1]))
        if k == len(part1.geometry.points) - 1:
            fid.write('\n')
        elif (k + 1) % 4 == 0:
            fid.write('\n            ')
        else:
            fid.write(', ')
    fid.write("   PART=%i\n" % 2)
    area = part2.get_area()
    EA = E * part2.get_area()
    eas = part2.get_eas()
    J = part2.get_ej()
    EI = part2.get_eic()
    bds = part2.geometry.geom.bounds
    cc = part2.get_c()
    cyp = bds[2] - cc[0]
    cym = cc[0] - bds[0]
    czp = bds[3] - cc[1]
    czm = cc[1] - bds[1]
    peri = part2.get_perimeter()
    fid.write("       %.0f, %.0f, %.0f, %.0f, %.5e, %.5e,%.5e\n" % (area, EA, eas[0], eas[1], J, EI[0], EI[1]))
    fid.write("       %.0f, %.0f, %.0f, %.0f, 0, 0, %.0f, 0, %.0f, %.0f\n" % (cyp, cym, czp, czm, peri, Cx, czm + 2000))
    fid.write("       %.0f, %.0f, %.0f, %.0f, " % (-cym, cyp, 0.5 * bot_width, -0.5 * bot_width))
    fid.write(" %.0f, %.0f, %.0f, %.0f\n" % (czp, czp, -czm, -czm))
    area = comp.get_area()
    EA = comp.get_ea(e_ref=C65)
    eas = comp.get_eas(e_ref=C65)
    J = comp.get_ej(e_ref=C65)
    EI = comp.get_eic(e_ref=C65)
    bds = comp.geometry.geom.bounds
    cc = comp.get_c()
    cyp = bds[2] - cc[0]
    cym = cc[0] - bds[0]
    czp = bds[3] - cc[1]
    czm = cc[1] - bds[1]
    peri = comp.get_perimeter()
    fid.write("       %.0f, %.0f, %.0f, %.0f, %.5e, %.5e,%.5e\n" % (EA, area, eas[0], eas[1], J, EI[0], EI[1]))
    fid.write("       %.0f, %.0f, %.0f, %.0f, 0, 0, %.0f, 0, %.0f, %.0f\n" % (cyp, cym, czp, czm, peri, Cx, czm))
    fid.write("       %.0f, %.0f, %.0f, %.0f, " % (-cym_p1, cyp_p1, 0.5 * bot_width, -0.5 * bot_width))
    fid.write(" %.0f, %.0f, %.0f, %.0f\n" % (czp - 258, czp - 258, -czm, -czm))
    fid.write("       1, NO, YES, 1.0, 0.2\n")
    fid.write("       OPOLY=%s" % poly_str)
    for k, pt in enumerate(part2.geometry.points):
        fid.write("%.6f, %.6f" % (pt[0], pt[1]))
        if k == len(part2.geometry.points) - 1:
            fid.write('\n')
        elif (k + 1) % 4 == 0:
            fid.write('\n            ')
        else:
            fid.write(', ')
    return


def comp_sections(wl, wr, is_end=False):
    if is_end:
        i_girder = un2ke(girder_type=1, material=C65)
    else:
        i_girder = un2k(girder_type=1, material=C65)
    i_girder.create_mesh(mesh_sizes=2000)
    I_sec = Section(geometry=i_girder)
    I_sec.calculate_geometric_properties()
    I_sec.calculate_warping_properties()
    I_sec.calculate_plastic_properties()

    slab1 = rectangular_section(d=225, b=wl + wr, material=C50).shift_section(x_offset=-wl, y_offset=100)
    slab2 = rectangular_section(d=100, b=1260, material=C50).shift_section(x_offset=-630)
    slab = slab1 + slab2
    slab.create_mesh(mesh_sizes=2000)
    Slab_sec = Section(geometry=slab)
    Slab_sec.calculate_geometric_properties()
    Slab_sec.calculate_warping_properties()
    Slab_sec.calculate_plastic_properties()

    comp_geom = i_girder + slab
    comp_geom.create_mesh(mesh_sizes=2000)
    comp_sec = Section(geometry=comp_geom)
    comp_sec.calculate_geometric_properties()
    comp_sec.calculate_warping_properties()
    comp_sec.calculate_plastic_properties()
    return I_sec, Slab_sec, comp_sec


if __name__ == '__main__':
    # wl, wr = 1850, 1550
    # i_girder = un2k(girder_type=1, material=C65)
    # i_girder.create_mesh(mesh_sizes=1000)
    # I_sec = Section(geometry=i_girder)
    # I_sec.calculate_geometric_properties()
    # I_sec.calculate_warping_properties()
    # I_sec.calculate_plastic_properties()
    # slab = rectangular_section(d=258, b=wl + wr, material=C50).shift_section(x_offset=-wl)
    # slab.create_mesh(mesh_sizes=1000)
    # Slab_sec = Section(geometry=slab)
    # Slab_sec.calculate_geometric_properties()
    # Slab_sec.calculate_warping_properties()
    # Slab_sec.calculate_plastic_properties()
    # comp_geom = i_girder + slab
    # comp_geom.create_mesh(mesh_sizes=1000)
    # comp_sec = Section(geometry=comp_geom)
    # comp_sec.calculate_geometric_properties()
    # comp_sec.calculate_warping_properties()
    # comp_sec.calculate_plastic_properties()
    # comp_sec.plot_mesh()
    i1, s1, c1 = comp_sections(1400, 1550)
    i2, s2, c2 = comp_sections(1550, 1400)
    fid = open("../res/csectons.mct", 'w+', encoding='GBK')
    fid.write("*UNIT\n")
    fid.write("   N    , MM, KJ, C\n")
    fid.write("*SECT-PSCVALUE\n")

    # fid.write(" SECT= 11, TAPERED, 跨中1 , CC,1, 0, 0, 0, 0, 0, 0, 0, YES, NO, CP_G, 1,1, YES, 1,2\n")
    # Part2MCT(fid, i1, s1, c1, 1400, 1010, E=1.0, poly_str="YES, ")
    # Part2MCT(fid, i2, s2, c2, 1550, 1010, E=1.0, poly_str="NO, ")

    fid.write(" SECT= 11, COMPOSITE-GEN, 跨中1 , CB, 0, 0, 0, 0, 0, 0, YES, NO, CP_G, YES, YES, 1\n")
    Part2MCT(fid, i1, s1, c1, 1400, 1010, E=1.0, poly_str="")
    fid.write(" SECT= 12, COMPOSITE-GEN, 跨中2 , CB, 0, 0, 0, 0, 0, 0, YES, NO, CP_G, YES, YES, 1\n")
    Part2MCT(fid, i2, s2, c2, 1550, 1010, E=1.0, poly_str="")
    fid.close()
