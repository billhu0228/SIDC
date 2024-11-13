from srbpy import Align

if __name__ == '__main__':
    D1 = Align('D1', '../Data/EI/D1')
    D2 = Align('D2', '../Data/EI/D2')
    D3 = Align('D3', '../Data/EI/D3')
    D4 = Align('D4', '../Data/EI/D4')
    M = Align('Mai', '../Data/EI/M')

    s1 = M.get_cross_slope(97.474)
    s2 = D2.get_elevation(180.364 - 4.5)
    print(s1)
