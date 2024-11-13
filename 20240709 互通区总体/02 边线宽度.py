from srbpy import Align
from functions import get_width

if __name__ == '__main__':
    D1 = Align('D1', '../Data/EI/D1')
    D2 = Align('D2', '../Data/EI/D2')
    D3 = Align('D3', '../Data/EI/D3')
    D4 = Align('D4', '../Data/EI/D4')
    M = Align('Mai', '../Data/EI/M')

    wl = get_width("边线.dxf", D1, 213.364, True, 'D2')
    wr = get_width("边线.dxf", D1, 213.364, False, 'D1')
    print(wl, wr)
