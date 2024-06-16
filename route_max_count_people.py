from coeff import *


def max_count_people(number_of_days, tur_obj):
    tur_obj.t = number_of_days
    rcc = tur_obj.calculate_rccq(tur_obj.calculate_pccq(tur_obj.calculate_bccq()))
    return rcc

# Входные данные
"""
    Кол-во дней, на которое нужно предельное значение, Туристический объект
"""
# print(max_count_people(30, TurObjWithoutTimeLim(name='Туристический объект без ограничений по времени', Cfn=[0.9, 0.83], MC=1, Ts=24, GS=7, t=30, routes=[OneDayTouristRouteWithoutTimeLim(DTp=10, DGp=1, Tdp=16, tp=1), OneDayTouristRouteWithoutTimeLim(DTp=12, DGp=1, Tdp=12, tp=1)])))
# Пример выхода
"""
    6117
"""