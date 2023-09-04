# units: mm N ton s
import numpy as np

g = 9.80665


def MM(inch: float):
    return 25.4 * inch


def INCH(mm: float):
    return 1.0 / MM(1.0) * mm


def TON(lb: float):
    return 0.45359237 * 1e-3 * lb


def LBS(ton: float):
    return 1.0 / TON(1.0) * ton


def LBF(newton: float):
    return LBS(newton / g / 1e3)


def NEWTON(lbf: float):
    return 1.0 / LBF(1.0) * lbf


def MPA(psi: float):
    return TON(psi) * g * 1000 / MM(1) / MM(1)


def PSI(mpa: float):
    return 1. / MPA(1.0) * mpa


def NPMM3(pcf: float):
    """
    磅每立方英尺 换算至 牛每立方毫米
    :param pcf:
    :return:
    """
    return pcf / (12.0 ** 3)


def get_fci_M(fc28: float, t: int):
    return t / (0.28 + 0.99 * t) * fc28


def get_Ec_ASTM_M(wc: float, fc: float):
    return 33 * np.power(wc, 1.5) * np.sqrt(fc)


if __name__ == "__main__":
    fci = PSI(36)
    wc = 140
    Eci = 33 * np.power(wc, 1.5) * np.sqrt(fci)
    print(MPA(Eci))
    print(MPA(0.24 * (np.sqrt(PSI(36.0) * 1e-3)) * 1000.0))
    print(MPA(0.24 * (np.sqrt(PSI(45.0) * 1e-3)) * 1000.0))
    print(MPA(0.19 * (np.sqrt(PSI(45.0) * 1e-3)) * 1000.0))
    k = 1
