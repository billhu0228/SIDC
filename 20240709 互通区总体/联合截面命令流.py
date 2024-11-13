import numpy as np


def my_range(c):
    tmp = c.split("to")
    s, e = [int(a) for a in tmp]
    return [int(a) for a in list(np.linspace(s, e, e - s + 1))]


if __name__ == '__main__':
    int_range = []
    int_range += my_range("7to13")
    int_range += my_range("189to191")
    int_range += my_range("34to37")
    int_range += my_range("46to49")
    int_range += my_range("56to59")
    int_range += my_range("68to71")
    int_range += my_range("80to83")
    int_range += my_range("90to93")
    int_range += my_range("102to105")
    int_range += my_range("114to117")
    int_range += my_range("126to129")
    int_range += my_range("138to141")
    int_range += my_range("148to151")
    int_range += my_range("158to161")
    int_range += my_range("170to173")
    int_range += my_range("182to185")
    print(int_range)
    print("*CPOSECT4CS")
    idlist = np.linspace(2, 194, 193)
    for id in idlist:
        if id in [5, 6, 9, 10, 11]:
            continue
        else:
            if id not in [20, 27, 28, 29, 30, 41, 42, 63, 64, 75, 76, 97, 98, 109, 110, 121, 122, 133, 134, 165, 166, 177, 178, ]:
                print("   SEC=%i, 梁体预制, GENERAL, NO" % id)
                print("       1, ELEM, , 梁体预制, 0, 1, 1, 1, 1, 1, 1, 1, 0.632336, 0")
            else:
                print("   SEC=%i, 简支转连续, GENERAL, NO" % id)
                print("       1, ELEM, , 简支转连续, 0, 1, 1, 1, 1, 1, 1, 1, 0.632336, 0")
            if id in int_range:
                print("       2, ELEM, , 跨中桥面板, 0, 1, 1, 1, 1, 1, 1, 1, 0.234449, 0")
            else:
                print("       2, ELEM, , 墩顶桥面板, 0, 1, 1, 1, 1, 1, 1, 1, 0.234449, 0")
