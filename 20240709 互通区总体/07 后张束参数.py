import os

import numpy as np


def read_specific_lines(file_path, start_line, end_line):
    num_lines = end_line - start_line + 1
    return np.loadtxt(file_path, skiprows=start_line - 1, max_rows=num_lines)


def find_lines_starting_with(file_path, search_string):
    line_numbers = []
    try:
        with open(file_path, 'r', encoding='gbk') as file:
            for line_number, line in enumerate(file, start=1):
                if line.startswith(search_string):
                    line_numbers.append(line_number)
    except Exception as e:
        print(f'Error processing file {file_path}: {e}')
    return line_numbers


def compute_adjacent_averages(lst):
    lst = np.array(lst)  # 将列表转换为 numpy 数组
    adjacent_averages = (lst[:-1] + lst[1:]) / 2
    return adjacent_averages


def get_allLength(strandsNo, isOneSide):
    """
    获取钢束长度
    :param data:
    :param strandsNo:
    :param isOneSide:
    :return: 理论长度，导管长度，下料长度
    """
    tLength = 0

    if strandsNo <= 18:
        AAnchorReserve = 0.75
    elif strandsNo <= 22:
        AAnchorReserve = 0.75
    elif strandsNo <= 27:
        AAnchorReserve = 0.80
    else:
        AAnchorReserve = 0.80

    if strandsNo <= 17:
        AAnchorB = 0.325
    elif strandsNo <= 22:
        AAnchorB = 0.325
    elif strandsNo <= 27:
        AAnchorB = 0.43
    else:
        AAnchorB = 0.43

    if strandsNo <= 17:
        AAnchorF = 0.075
    elif strandsNo <= 19:
        AAnchorF = 0.075
    elif strandsNo <= 22:
        AAnchorF = 0.08
    elif strandsNo <= 24:
        AAnchorF = 0.082
    elif strandsNo <= 27:
        AAnchorF = 0.085
    else:
        AAnchorF = 0.085

    if strandsNo <= 17:
        PAnchorB = 0.72
    elif strandsNo <= 19:
        PAnchorB = 0.72
    elif strandsNo <= 22:
        PAnchorB = 0.90
    elif strandsNo <= 27:
        PAnchorB = 1.0
    else:
        raise NotImplementedError
    tLength = np.round(tLength, 4)
    if isOneSide:
        DuctLength = np.round(tLength - AAnchorB - 0.02 - PAnchorB, 4)
        Length = np.round(0.2 + AAnchorReserve + 0.020 + AAnchorF * 3 + tLength + 0.2, 4)
    else:
        DuctLength = np.round(tLength - 2 * (AAnchorB + 0.02), 4)
        Length = np.round(2 * (0.2 + AAnchorReserve + 0.020 + AAnchorF * 3) + tLength, 4)
    return tLength, DuctLength, Length


if __name__ == '__main__':
    config = {
        'R26-W17': ['30+3x45', [10, 10, 10, 10]],
        'R16-W17': ['R1-3x45', [10, 10, 10, 10]],
        'W14-W17': ['W14-W17', [8, 8, 8, 8]],
        'SA-R21': ['SA-R21', [10, 10, 12, 12]],
        'R31-NA': ['R31-NA', [12, 12, 14, 14]],
        'R15R16': ['R15R16', [14, 14, 16, 16]],
    }
    for key in config.keys():
        cwd = r'D:\20240113 SIDC项目\Midas模型\预应力损失\%s' % (config[key][0])
        nop_list = config[key][1]
        print(f"{key}:")
        for _, _, files in os.walk(cwd):
            for f in files:
                file = os.path.join(cwd, f)
                idx = int(file[-1]) - 1
                st, ed = find_lines_starting_with(file, "----")
                data = read_specific_lines(file, st + 1, ed - 1)
                ds = np.diff(data[:, 0])
                sigma = compute_adjacent_averages(data[:, 1]) / (nop_list[idx] * 140)
                Es = 197e3
                eps = sigma / Es
                dl = eps * ds
                TheL, DuctL, WorkL = get_allLength(nop_list[idx], False)
                BaseLength = sum(ds) * 1e-3
                elong = sum(dl) * 1e-3
                # print(f'{f}, 钢束长度={}m')
                print("  %s: 下料 = %8.3f m | 导管 = %8.3f m | 伸长量 = %8.3f mm" % (f, WorkL + BaseLength, DuctL + BaseLength, elong))

                # break
