from src.sections import DXFSection

if __name__ == "__main__":
    S45 = DXFSection(1, "S45", './src/NU2000.dxf', 2000)
    # info_pre = StressInfo(1860 * 0.75, 42 * 140, -633.04, -1269.9543)
    S45.addStrand(929.95 - 633.04, 0.9 * 1860, 42 * 140)
    w = S45.get_sum_N(100)

    print(w)
