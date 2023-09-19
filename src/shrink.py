def beta_shrink(t, t0, A, u):
    h = 2 * A / u
    A = t - t0
    B = (350 * (h / 100) ** 2) + A
    return (A / B) ** 0.5


def eps_s(fcm, beta_sc):
    """
    受混凝土强度影响的收缩应变
    :param fcm:
    :param beta_sc:
    :return:
    """
    return (160 + 10 * beta_sc * (9 - fcm / 10.0)) * 1e-6


def beta_RH(RH):
    """
    收缩系数
    :param RH: 湿度
    :return:
    """
    if RH >= 0.99:
        return 0.25
    elif RH >= 0.4:
        bsrh = 1 - (RH) ** 3
        return -1.55 * bsrh
    else:
        raise Exception()


def shrink_eps(t, t0, fc, beta_sc, RH, A, u):
    return eps_s(fc, beta_sc) * beta_RH(RH) * beta_shrink(t, t0, A, u)
