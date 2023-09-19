def TDNProfile(ele: str, span_label: str, x0, x1):
    profile = [
        [8, 4, 2, 0],
        [8, 0, 4, 2],
        [6, 0, 0, 2],
        [4, 0, 0, 0],
    ]
    k = ["", 'a', 'b', 'c']
    dx = [0, 1500, 3000, 4500]
    ret = ""
    for i, y in enumerate([75, 125, 175, 1955]):
        for j in range(4):
            num = profile[i][j]
            ddx = dx[j]
            name = span_label + str(i + 1) + k[j]
            if num != 0:
                ret += "   NAME=%s, S%i, %s, 0, 0, ROUND, 2D\n" % (name, num, ele)
                ret += "      先张束, USER, 0, 0, NO, \n"
                ret += "      STRAIGHT, 0, 0, 0, X, 0, 0\n"
                ret += "      0, YES, Y, 0\n"
                ret += "      Y=%i, 0, NO, 0, 0, NONE, , , , \n" % (x0 + ddx)
                ret += "      Y=%i, 0, NO, 0, 0, NONE, , , , \n" % (x1 - ddx)
                ret += "      Z=%i, %i, NO, 0, 0, NONE, , , , \n" % (x0 + ddx, y)
                ret += "      Z=%i, %i, NO, 0, 0, NONE, , , , \n" % (x1 - ddx, y)
    return ret


def post_tendon(ele, xlist, ylist, label, no=12):
    ret = ""
    name = label
    ret += "   NAME=%s, P%i, %s, 0, 0, ROUND, 2D\n" % (name, no, ele)
    ret += "      后张束, USER, 0, 0, NO, \n"
    ret += "      STRAIGHT, 0, 0, 0, X, 0, 0\n"
    ret += "      0, YES, Y, 0\n"
    ret += "      Y=%i, 0, NO, 0, 0, NONE, , , , \n" % xlist[0]
    ret += "      Y=%i, 0, NO, 0, 0, NONE, , , , \n" % xlist[-1]
    for i, x in enumerate(xlist):
        y = ylist[i]
        ret += "      Z=%i, %i, NO, 0, 0, NONE, , , , \n" % (x, y)
    return ret


def get_vertical_val(spans, x0, zval):
    xs = []
    z1, z2, z3 = zval
    zs = [z1]
    for i, sp in enumerate(spans):
        if i == 0:
            xs += [13000, sp - 27000, 11500, 2500]
            zs += [z2, z2, z3, z3]
        elif i == len(spans) - 1:
            xs += [2500, 11500, sp - 27000, 13000]
            zs += [z3, z2, z2, z1]
        else:
            xs += [2500, 11000, sp - 27000, 11000, 2500]
            zs += [z3, z2, z2, z3, z3]
    new_x = [x0]
    for j in xs:
        new_x.append(new_x[-1] + j)
    return new_x, zs


if __name__ == "__main__":
    txt = "*TDN-PROFILE\n"
    # txt += TDNProfile("101to145", "A", 260, 44750)
    # txt += TDNProfile("201to245", "B", 45250, 89750)
    # txt += TDNProfile("301to345", "C", 90250, 134750)
    # txt += TDNProfile("401to445", "D", 135250, 179740)

    all_ele = "1to6 101to145 201to245 301to345 401to445"

    xx1, zz1 = get_vertical_val([44740, 45000, 45000, 44740], 260, [1750, 680, 1900])
    xx2, zz2 = get_vertical_val([44740, 45000, 45000, 44740], 260, [1350, 560, 1780])
    xx3, zz3 = get_vertical_val([44740, 45000, 45000, 44740], 260, [950, 440, 1460])
    xx4, zz4 = get_vertical_val([44740, 45000, 45000, 44740], 260, [550, 320, 1340])
    txt += post_tendon(all_ele, xx1, zz1, "T1")
    txt += post_tendon(all_ele, xx2, zz2, "T2")
    txt += post_tendon(all_ele, xx3, zz3, "T3")
    txt += post_tendon(all_ele, xx4, zz4, "T4")
    print(txt)
