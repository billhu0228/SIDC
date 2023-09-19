def beta_c(Ac, u, RH, t, t0):
    """
    徐变发展系数
    :param t0: 初始加载 (day)
    :param t:  考虑时间 (day)
    :param Ac: 面积 (mm)
    :param u: 周长 (mm)
    :param RH: 相对湿度 (0~1.0)
    :return:
    """
    h = 2 * Ac / u
    beta_H = 150 * (1 + (1.2 * RH) ** 18) * (h / 100.0) + 250
    if beta_H > 1500:
        beta_H = 1500
    return ((t - t0) / (beta_H + (t - t0))) ** 0.3


def phi_0(Ac, u, RH, fcm, t0):
    """
    名义徐变系数
    :param t0: 加载初始日
    :param fcm: 标号
    :param Ac: 面积 (mm)
    :param u: 周长 (mm)
    :param RH: 相对湿度 (0~1.0)
    :return:
    """
    h = 2 * Ac / u
    phi_RH = 1 + (1 - RH) / (0.46 * (h / 100) ** (1 / 3))
    beta_fcm = 5.3 / (fcm / 10.0) ** 0.5
    beta_t0 = 1 / (0.1 + t0 ** 0.2)
    return phi_RH * beta_fcm * beta_t0


def creep_coff(t, t0, A, u, RH, fc):
    """
    徐变系数（FIP-CEB 1990)
    :param t: 考虑时间
    :param t0: 加载时间
    :param A: 面积 (mm)
    :param u: 周长 (mm)
    :param RH: 相对湿度 (0~1.0)
    :param fc: 混凝土标号
    :return:
    """
    p0 = phi_0(A, u, RH, fc, t0)
    bc = beta_c(A, u, RH, t, t0)
    return p0 * bc


def Kid(t, t0, A, u, RH, fc, Eci, Ep, I, Aps, ec):
    """
    滑移系数
    :param t:
    :param t0:
    :param A:
    :param u:
    :param RH:
    :param fc:
    :param Eci:
    :param Ep:
    :param I:
    :param Aps:
    :param ec:
    :return:
    """
    psi_b = creep_coff(t, t0, A, u, RH, fc)
    A = (Ep / Eci) * (Aps / A)
    B = (1 + A * ec ** 2 / I)
    C = (1 + 0.7 * psi_b)
    return (1 + A * B * C) ** -1
