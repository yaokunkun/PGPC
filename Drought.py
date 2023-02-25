from math import exp
from random import randint, random
import numpy as np


def Drought(frequency: int, duration_average: int, duration_diff: int, P_average: float, P_diff: float,
            T_average: float, T_diff: float, T_drought: float):
    """
    模拟干旱条件，改变降水量数组P，PAE数组，气温数组T
    :param frequency: 模拟的一年中干旱次数
    :param duration_average: 平均持续时间（天）
    :param duration_diff: 干旱持续时间波动（天）
    :param P_average: 下雨时年平均降水量
    :param P_diff: 降水量波动
    :param T_average: 下雨时年平均气温
    :param T_diff: 下雨时气温波动
    :param T_drought: 干旱时气温
    :return: P, T: 一年之中的降水量、气温列表
    """
    P_rain = np.full(365, P_average) + np.random.rand(365) * P_diff
    T_rain = np.full(365, T_average) + np.random.rand(365) * T_diff
    # P_rain_sunny = [P * randint(0,1) for P in P_rain]
    P = P_rain.tolist()
    T = T_rain.tolist()
    frag = 365 // frequency
    start_days = [frag * i for i in range(frequency)]
    end_days = [start_day + duration_average + randint(-duration_diff, duration_diff) for start_day in start_days]
    # sun_time = 265
    for i in range(frequency):
        start_day = start_days[i]
        end_day = end_days[i]

        # 但是干旱期间，也需要下雨，就模拟在[start_day, end_day)区间的最中间10±2天恢复正常
        mid = (start_day + end_day) // 2
        drought_rain_start = mid - 5 + randint(-1, 1)
        drought_rain_end = mid + 5 + randint(-1, 1)
        P[start_day: drought_rain_start] = [0] * (drought_rain_start - start_day)
        P[drought_rain_end: end_day] = [0] * (end_day - drought_rain_end)
        T[start_day: drought_rain_start] = [T_drought + random() * T_diff * 2 for _ in
                                            range(start_day, drought_rain_start)]
        T[drought_rain_end: end_day] = [T_drought + random() * T_diff * 2 for _ in range(drought_rain_end, end_day)]

        drought_sun_start = mid - 1 + randint(-1, 1)
        drought_sun_end = mid + 1 + randint(-1, 1)
        P[drought_sun_start: drought_sun_end] = [0] * (drought_sun_end - drought_sun_start)
        T[drought_sun_start: drought_sun_end] = [T_drought + random() * T_diff * 2 for _ in
                                                 range(drought_sun_start, drought_sun_end)]

    # 在每次干旱之间插入晴天
    # while sun_time > 0:
    for i in range(frequency - 1):
        curr_end_day = end_days[i]
        next_start_day = start_days[i + 1]

        curr_day = curr_end_day
        while curr_day < next_start_day:
            curr_day += randint(2, 5)  # 下2~5天雨
            sum_end_day = curr_day + randint(2, 5)  # 再出2~5天太阳
            if sum_end_day < next_start_day:
                P[curr_day: sum_end_day] = [0] * (sum_end_day - curr_day)
                T[curr_day: sum_end_day] = [(T_drought + T_average) / 2 + random() * T_diff * 2 for _ in
                                            range(curr_day, sum_end_day)]
                curr_day = sum_end_day
    # 现对最后一次干旱与第365天之间插入晴天
    curr_day = end_days[-1]
    while curr_day < 365:
        curr_day += randint(2, 5)  # 下2~5天雨
        sum_end_day = curr_day + randint(2, 5)  # 再出2~5天太阳
        if sum_end_day < 365:
            P[curr_day: sum_end_day] = [0] * (sum_end_day - curr_day)
            T[curr_day: sum_end_day] = [(T_drought + T_average) / 2 + random() * T_diff * 2 for _ in
                                        range(curr_day, sum_end_day)]
            curr_day = sum_end_day

    count = 0
    for i in range(365):
        if P[i] == 0:
            count += 1
    print(count)

    # 调换一下最开始的干旱期和最后的正常期
    P_temp = P[end_days[-1]:]
    T_temp = T[end_days[-1]:]
    P[365 - end_days[-1]:] = P[0:end_days[-1]]
    T[365 - end_days[-1]:] = T[0:end_days[-1]]
    P[0:365 - end_days[-1]] = P_temp
    T[0:365 - end_days[-1]] = T_temp
    return P, T


frequency = 3
duration_ave = 60
duration_diff = 15
T_ave = 8
T_diff = 1
T_drought = 20
P, T = Drought(frequency, duration_ave, duration_diff, 3, 1, T_ave, T_diff, T_drought)

PAR = [3.496 * exp(0.0605 * T_) for T_ in T] + [random() * 2.41] * len(T)
PET = [0.0844 * exp(0.0913 * T_) for T_ in T] + [random() * 0.84] * len(T)
print(PET)
