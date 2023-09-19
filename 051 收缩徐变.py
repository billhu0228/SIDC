import src as ss

if __name__ == "__main__":
    area = ss.A
    u_dia = 7483.19
    cr5 = ss.creep_coff(10000, 190, ss.A, u_dia, 0.8, 70.0)
    cr4 = ss.creep_coff(190, 186, ss.A, u_dia, 0.8, 70.0)
    cr3 = ss.creep_coff(186, 183, ss.A, u_dia, 0.8, 70.0)
    cr2 = ss.creep_coff(183, 180, ss.A, u_dia, 0.8, 70.0)
    cr1 = ss.creep_coff(180, 7, ss.A, u_dia, 0.8, 70.0)
    cr0 = ss.creep_coff(7, 0, ss.A, u_dia, 0.8, 70.0)
    Kid = ss.Kid(180, 7, area, u_dia, 0.8, 70, ss.Ec, ss.Ep, ss.I, Aps=42 * 140.0, ec=633.0452380952381)
    Kid2 = ss.Kid(183, 180, area, u_dia, 0.8, 70, ss.Ec, ss.Ep, ss.I, Aps=42 * 140.0, ec=633.0452380952381)
    Kid3 = ss.Kid(186, 183, area, u_dia, 0.8, 70, ss.Ec, ss.Ep, ss.I, Aps=42 * 140.0, ec=633.0452380952381)
    Kid4 = ss.Kid(190, 186, area, u_dia, 0.8, 70, ss.Ec, ss.Ep, ss.I, Aps=42 * 140.0, ec=633.0452380952381)
    Kid5 = ss.Kid(10000, 190, area, u_dia, 0.8, 70, ss.Ec, ss.Ep, ss.I, Aps=42 * 140.0, ec=633.0452380952381)
    print(cr5, Kid5)

    print(ss.creep_coff(10000, 7, ss.A, u_dia, 0.8, 70.0))

    eps_sk = ss.shrink_eps(180, 7, 70, 5, 0.8, ss.A, ss.outer)
    print(eps_sk * ss.Ep * Kid)

    eps_sk = ss.shrink_eps(183, 180, 70, 5, 0.8, ss.A, ss.outer)
    print(eps_sk * ss.Ep * Kid2)

    eps_sk = ss.shrink_eps(186, 183, 70, 5, 0.8, ss.A, ss.outer)
    print(eps_sk * ss.Ep * Kid3)

    eps_sk = ss.shrink_eps(10000, 190, 70, 5, 0.8, ss.A, ss.outer)
    print(eps_sk * ss.Ep * Kid5)
