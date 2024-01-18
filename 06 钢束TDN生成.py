def TDNProfile(ele: str, span_label: str, x0, x1, z):
    profile = [
        [8, 4, 2, 0],
        [8, 0, 4, 2],
        [6, 0, 0, 2],
        [2, 0, 0, 0],
        [4, 0, 0, 0],
    ]
    k = ["", 'a', 'b', 'c']
    dx = [0, 1500, 3000, 4500]
    ret = ""
    for i, y in enumerate([75, 125, 175, 225, 1955]):
        for j in range(4):
            num = profile[i][j]
            ddx = dx[j]
            name = span_label + str(i + 1) + k[j]
            if num != 0:
                ret += "   NAME=%s, S%i, %s, 0, 0, ROUND, 2D\n" % (name, num, ele)
                ret += "      先张束, USER, 0, 0, NO, \n"
                ret += "      STRAIGHT, 0, 0, 0, X, 0, 0\n"
                ret += "      0, YES, Y, 0\n"
                ret += "      Y=%i, %i, NO, 0, 0, NONE, , , , \n" % (x0 + ddx, z)
                ret += "      Y=%i, %i, NO, 0, 0, NONE, , , , \n" % (x1 - ddx, z)
                ret += "      Z=%i, %i, NO, 0, 0, NONE, , , , \n" % (x0 + ddx, y)
                ret += "      Z=%i, %i, NO, 0, 0, NONE, , , , \n" % (x1 - ddx, y)
    return ret


def post_tendon(ele, xlist, ylist, label, z, no=12):
    ret = ""
    name = label
    ret += "   NAME=%s, P%i, %s, 0, 0, ROUND, 2D\n" % (name, no, ele)
    ret += "      后张束, USER, 0, 0, NO, \n"
    ret += "      STRAIGHT, 0, 0, 0, X, 0, 0\n"
    ret += "      0, YES, Y, 0\n"
    ret += "      Y=%i, %i, NO, 0, 0, NONE, , , , \n" % (xlist[0], z)
    ret += "      Y=%i, %i, NO, 0, 0, NONE, , , , \n" % (xlist[-1], z)
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


def pre():
    txt = "*TDN-PROFILE\n"
    txt += TDNProfile("1000to1048", "1A", 260, 44750, 6000)
    txt += TDNProfile("1051to1099", "1B", 45250, 89750, 6000)
    txt += TDNProfile("1102to1150", "1C", 90250, 134740, 6000)
    txt += TDNProfile("2000to2048", "2A", 260, 44750, 3000)
    txt += TDNProfile("2051to2099", "2B", 45250, 89750, 3000)
    txt += TDNProfile("2102to2150", "2C", 90250, 134740, 3000)
    txt += TDNProfile("3000to3048", "3A", 260, 44750, 0)
    txt += TDNProfile("3051to3099", "3B", 45250, 89750, 0)
    txt += TDNProfile("3102to3150", "3C", 90250, 134740, 0)
    print(txt)


def pre30_3x45():
    txt = "*TDN-PROFILE\n"
    txt += TDNProfile("1000to1032", "1A", 260, 29750, 3100)
    txt += TDNProfile("1035to1083", "1B", 30250, 74750, 3100)
    txt += TDNProfile("1086to1134", "1C", 75250, 119750, 3100)
    txt += TDNProfile("1137to1185", "1D", 120250, 164740, 3100)
    txt += TDNProfile("2000to2032", "2A", 260, 29750, 0)
    txt += TDNProfile("2035to2083", "2B", 30250, 74750, 0)
    txt += TDNProfile("2086to2134", "2C", 75250, 119750, 0)
    txt += TDNProfile("2137to2185", "2D", 120250, 164740, 0)
    print(txt)


def pre3x40():
    txt = "*TDN-PROFILE\n"
    txt += TDNProfile("1000to1043", "1A", 260, 39750, 6300)
    txt += TDNProfile("1046to1089", "1B", 40250, 79750, 6300)
    txt += TDNProfile("1092to1135", "1C", 80250, 119740, 6300)
    txt += TDNProfile("2000to2043", "2A", 260, 39750, 4200)
    txt += TDNProfile("2046to2089", "2B", 40250, 79750, 4200)
    txt += TDNProfile("2092to2135", "2C", 80250, 119740, 4200)
    txt += TDNProfile("3000to3043", "3A", 260, 39750, 2100)
    txt += TDNProfile("3046to3089", "3B", 40250, 79750, 2100)
    txt += TDNProfile("3092to3135", "3C", 80250, 119740, 2100)
    txt += TDNProfile("4000to4043", "4A", 260, 39750, 0)
    txt += TDNProfile("4046to4089", "4B", 40250, 79750, 0)
    txt += TDNProfile("4092to4135", "4C", 80250, 119740, 0)
    print(txt)


def mct_post():
    txt = "*TDN-PROFILE\n"
    for i in range(3):
        n = i + 1
        all_ele = "%s000to%s150" % (n, n)  #
        xx1, zz1 = get_vertical_val([44740, 45000, 44740], 260, [1750, 680, 1900])
        xx2, zz2 = get_vertical_val([44740, 45000, 44740], 260, [1350, 560, 1780])
        xx3, zz3 = get_vertical_val([44740, 45000, 44740], 260, [950, 440, 440])
        xx4, zz4 = get_vertical_val([44740, 45000, 44740], 260, [550, 320, 320])
        txt += post_tendon(all_ele, xx1, zz1, "%sT1" % n, (2 - i) * 3000)
        txt += post_tendon(all_ele, xx2, zz2, "%sT2" % n, (2 - i) * 3000)
        txt += post_tendon(all_ele, xx3, zz3, "%sT3" % n, (2 - i) * 3000)
        txt += post_tendon(all_ele, xx4, zz4, "%sT4" % n, (2 - i) * 3000)
    print(txt)


def mct_post3x40():
    txt = "*TDN-PROFILE\n"
    for i in range(4):
        n = i + 1
        all_ele = "%s000to%s135" % (n, n)  #
        xx1, zz1 = get_vertical_val([39740, 40000, 39740], 260, [1750, 680, 1900])
        xx2, zz2 = get_vertical_val([39740, 40000, 39740], 260, [1350, 560, 1780])
        xx3, zz3 = get_vertical_val([39740, 40000, 39740], 260, [950, 440, 440])
        xx4, zz4 = get_vertical_val([39740, 40000, 39740], 260, [550, 320, 320])
        txt += post_tendon(all_ele, xx1, zz1, "%sT1" % n, (3 - i) * 2100)
        txt += post_tendon(all_ele, xx2, zz2, "%sT2" % n, (3 - i) * 2100)
        txt += post_tendon(all_ele, xx3, zz3, "%sT3" % n, (3 - i) * 2100)
        txt += post_tendon(all_ele, xx4, zz4, "%sT4" % n, (3 - i) * 2100)
    print(txt)


def mct_post30_3x45():
    txt = "*TDN-PROFILE\n"
    for i in range(2):
        n = i + 1
        all_ele = "%s000to%s185" % (n, n)  #
        xx1, zz1 = get_vertical_val([29740, 45000, 45000, 44740], 260, [1750, 680, 1900])
        xx2, zz2 = get_vertical_val([29740, 45000, 45000, 44740], 260, [1350, 560, 1780])
        xx3, zz3 = get_vertical_val([29740, 45000, 45000, 44740], 260, [950, 440, 440])
        xx4, zz4 = get_vertical_val([29740, 45000, 45000, 44740], 260, [550, 320, 320])
        txt += post_tendon(all_ele, xx1, zz1, "%sT1" % n, (1 - i) * 3100)
        txt += post_tendon(all_ele, xx2, zz2, "%sT2" % n, (1 - i) * 3100)
        txt += post_tendon(all_ele, xx3, zz3, "%sT3" % n, (1 - i) * 3100)
        txt += post_tendon(all_ele, xx4, zz4, "%sT4" % n, (1 - i) * 3100)
    print(txt)


if __name__ == "__main__":
    # mct_post30_3x45()
    # pre30_3x45()
    # pre()
    # pre3x40()
    mct_post3x40()
    # txt = "*TDN-PROFILE\n"
    # txt += TDNProfile("1000to1048", "1A", 260, 44750)
    # txt += TDNProfile("201to245", "1B", 45250, 89750)
    # txt += TDNProfile("301to345", "1C", 90250, 134750)
    # txt += TDNProfile("401to445", "1D", 135250, 179740)
    # txt = "*TDN-PROFILE\n"
    # txt += TDNProfile("1to45", "A", 260, 44750)
    # txt += TDNProfile("48to92", "B", 45250, 89750)
    # txt += TDNProfile("95to139", "C", 90250, 134750)
    # txt += TDNProfile("142to186", "D", 135250, 179750)
    # txt += TDNProfile("189to233", "E", 180250, 224740)
    # all_ele = "1to228"  #
    # xx1, zz1 = get_vertical_val([44740, 45000, 45000, 45000, 44740], 260, [1750, 680, 1900])
    # xx2, zz2 = get_vertical_val([44740, 45000, 45000, 45000, 44740], 260, [1350, 560, 1780])
    # xx3, zz3 = get_vertical_val([44740, 45000, 45000, 45000, 44740], 260, [950, 440, 440])
    # xx4, zz4 = get_vertical_val([44740, 45000, 45000, 45000, 44740], 260, [550, 320, 320])

    # xx1, zz1 = get_vertical_val([44740, 45000, 45000, 45000, 34830], 260, [1750, 680, 1900])
    # xx2, zz2 = get_vertical_val([44740, 45000, 45000, 45000, 34830], 260, [1350, 560, 1780])
    # xx3, zz3 = get_vertical_val([44740, 45000, 45000, 45000, 34830], 260, [950, 440, 440])
    # xx4, zz4 = get_vertical_val([44740, 45000, 45000, 45000, 34830], 260, [550, 320, 320])
    # txt += post_tendon(all_ele, xx1, zz1, "T1")
    # txt += post_tendon(all_ele, xx2, zz2, "T2")
    # txt += post_tendon(all_ele, xx3, zz3, "T3")
    # txt += post_tendon(all_ele, xx4, zz4, "T4")

    # txt = "*TDN-PROFILE\n"
    # txt += TDNProfile("1to46", "A", 260, 44750)
    # txt += TDNProfile("49to94", "B", 45250, 89750)
    # txt += TDNProfile("97to142", "C", 90250, 134750)
    # txt += TDNProfile("145to190", "D", 135250, 179750)
    # txt += TDNProfile("193to228", "E", 180250, 214830)
    # print(txt)
