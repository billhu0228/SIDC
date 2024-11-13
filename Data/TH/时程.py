import numpy as np
import pandas as pd

if __name__ == '__main__':
    with open("th.mct", 'r', encoding='gbk') as fid:
        ll = fid.readlines()
    res = []
    name = 'null'
    th = []
    for line in ll:
        if line.__contains__("FUNC=") or line.__contains__('end'):
            print(line)
            res.append((name, th))
            th = []
            name = line.split('=')[-1].split()
        elif line == '\n':
            continue
        else:
            dd = [float(a) for a in line.split(',')]
            if len(dd) == 4:
                th.append(dd[0:2])
                th.append(dd[2:4])
            elif len(dd) == 2:
                th.append(dd[0:2])
            else:
                raise Exception()
    res.remove(res[0])
    T = []
    # col = {}
    for th in res:
        T.append([s[0] for s in th[1]])
        T.append([s[1] for s in th[1]])
        # col.append('time')
        # col.append(th[0])
    mat = pd.DataFrame(T).T
    mat.to_excel('TH-SIDC.xlsx')
