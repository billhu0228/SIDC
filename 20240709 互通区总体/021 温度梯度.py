import pandas as pd

if __name__ == '__main__':
    data = pd.read_excel('./SS/SS模型参数.xlsx', sheet_name='单元表', header=None)
    #     print("*USE-STLD, 梯度升温")
    #     print("*BSTEMPER ")
    #     for i, row in data.iterrows():
    #         print("  %i, LZ, Top, 3, , NO" % (row[0]))
    #         print("    ELEMENT,  0, 0,  3100,  0, 30,  100, 7.8")
    #         print("    ELEMENT,  0, 0,  3100,  100, 7.8,  225, 4.55")
    #         print("    ELEMENT,  0, 0,  1260,  225, 4.55,  400, 0")

    print("*USE-STLD, 梯度降温")
    print("*BSTEMPER ")
    for i, row in data.iterrows():
        print("  %i, LZ, Top, 3, , NO" % (row[0]))
        print("    ELEMENT,  0, 0,  3100,  0, -9,  100, -2.34")
        print("    ELEMENT,  0, 0,  3100,  100, -2.34,  225, -1.365")
        print("    ELEMENT,  0, 0,  1260,  225, -1.365,  400, 0")
