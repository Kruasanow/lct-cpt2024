from typing import List


def calculate_rccoopt(RCCqms: list[int]):
    """
    :param RCCqms: массив предельно допустимых рекреационных емкостей туристских объектов, человек в единицу времени
    :return: Предельно допустимая рекреационная емкость особо охраняемой природной территории
    """
    return sum(RCCqms)


class TurObj:
    def __init__(self, name: str, Cfn: list[float], MC: float):
        """
        Туристический объект
        :param name: название
        :param Cfn (list[float]): поправочные коэффициенты, которые учитывают определенные для туристских объектов лимитирующие факторы развития туризма (экологического, социального и социокультурного характера) и установленные режимы использования туристских объектов
        :param MC (float): коэффициент управленческой емкости, долей от единицы
        """
        self.name = name
        self.Cfn = Cfn
        self.MC = MC

    def calculate_pccq(self, BCCq: int):
        """
        :param BCCq: базовая рекреационная емкость туристского объекта, выраженная в целочисленном значении, человек в единицу времени
        :return: Потенциальная рекреационная емкость туристского объекта
        """
        product_Cfn = 1
        for Cf in self.Cfn:
            product_Cfn *= Cf
        return int(BCCq * product_Cfn)

    def calculate_rccq(self, PCCq: int):
        """
        :param PCCq: потенциальная рекреационная емкость туристского объекта, человек в единицу времени
        :return: Предельно допустимая рекреационная емкость туристского объекта
        """
        return int(PCCq * self.MC)


class TurObjArea(TurObj):
    def __init__(self, name, Cfn, MC, A: float, Au: float, T: float, Td: float, t: int):
        """
        :param name: название
        :param Cfn (list[float]): поправочные коэффициенты, которые учитывают определенные для туристских объектов лимитирующие факторы развития туризма (экологического, социального и социокультурного характера) и установленные режимы использования туристских объектов
        :param MC (float): коэффициент управленческой емкости, долей от единицы
        :param A: площадь туристского объекта, на которой осуществляется туризм, кв. метров
        :param Au: площадь туристского объекта, необходимая для одного посетителя при осуществлении туризма (кв. метров)
        :param T: количество часов в сутки, когда туристский объект доступен для посещения, часов
        :param Td: среднее время пребывания посетителя на туристском объекте, часов
        :param t: количество дней в рассматриваемую единицу времени (месяц, сезон, год и др.), единиц
        """
        super().__init__(name, Cfn, MC)
        self.A = A
        self.Au = Au
        self.T = T
        self.Td = Td
        self.t = t

    def calculate_bccq(self):
        """
        :return: Базовая рекреационная емкость
        """
        return int((self.A / self.Au) * self.__calculate_rf() * self.t)

    def __calculate_rf(self):
        """
        :return: Коэффициент возвращения
        """
        return self.T / self.Td


class OneDayTouristRouteWithoutTimeLim:
    def __init__(self, DTp: float, DGp: float, Tdp: float, tp: int):
        """
        :param DTp: длина однодневного туристского маршрута или однодневного участка p многодневного туристского маршрута в дневной переход, км
        :param DGp: оптимальное расстояние между группами на участке p туристского маршрута, км
        :param Tdp: среднее время прохождения участка туристского маршрута p с учетом остановок, часов
        :param tp: количество дней пребывания посетителей на туристском маршруте, единиц
        """
        # self.name = name
        self.DTp = DTp
        self.DGp = DGp
        self.Tdp = Tdp
        self.tp = tp


class TurObjWithoutTimeLim(TurObj):
    def __init__(self, name, Cfn, MC, Ts: float, GS: int, t: int, routes: List[OneDayTouristRouteWithoutTimeLim]):
        """
        :param name: название
        :param Cfn (list[float]): поправочные коэффициенты, которые учитывают определенные для туристских объектов лимитирующие факторы развития туризма (экологического, социального и социокультурного характера) и установленные режимы использования туристских объектов
        :param MC (float): коэффициент управленческой емкости, долей от единицы
        :param Ts: длина светового дня или количество времени, когда туристский маршрут доступен для посетителей, часов
        :param GS: среднее количество человек в группе (включая сопровождающих), человек
        :param t: количество дней в рассматриваемую единицу времени (месяц, сезон, год и др.), единиц
        :param routes: лист экземпляров однодневных маршрутов/участков
        """
        super().__init__(name, Cfn, MC)
        self.routes = routes
        self.Ts = Ts
        self.GS = GS
        self.t = t

    def calculate_bccq(self):
        """
        :return: Базовая рекреационная емкость
        """
        bccq = 0
        for route in self.routes:
            bccq += (route.DTp / route.DGp) * (self.Ts / route.Tdp) * self.GS * (self.t / route.tp)
        return bccq


class OneDayTouristRouteWithTimeLim:
    def __init__(self, DGp: float, Tdp: float, tp: int, vp: float):
        """
        :param DGp: оптимальное расстояние между группами на участке p туристского маршрута, км
        :param Tdp: среднее время прохождения участка туристского маршрута p с учетом остановок, часов
        :param tp: количество дней пребывания посетителей на туристском маршруте, единиц
        :param vp: средняя скорость передвижения по однодневному участку p туристского маршрута с учетом остановок, км в час
        """
        self.DGp = DGp
        self.Tdp = Tdp
        self.tp = tp
        self.vp = vp


class TurObjWithTimeLim(TurObj):
    def __init__(self, name, Cfn, MC, Ts: float, GS: int, t: int, routes: List[OneDayTouristRouteWithTimeLim]):
        """
        :param name: название
        :param Cfn (list[float]): поправочные коэффициенты, которые учитывают определенные для туристских объектов лимитирующие факторы развития туризма (экологического, социального и социокультурного характера) и установленные режимы использования туристских объектов
        :param MC (float): коэффициент управленческой емкости, долей от единицы
        :param Ts: длина светового дня или количество времени, когда туристский маршрут доступен для посетителей, часов
        :param GS: среднее количество человек в группе (включая сопровождающих), человек
        :param t: количество дней в рассматриваемую единицу времени (месяц, сезон, год и др.), единиц
        :param routes: лист экземпляров однодневных маршрутов/участков
        """
        super().__init__(name, Cfn, MC)
        self.routes = routes
        self.Ts = Ts
        self.GS = GS
        self.t = t

    def calculate_bccq(self):
        """
        :return: Базовая рекреационная емкость: float
        """
        bccq = 0
        for route in self.routes:
            bccq += (self.__calculate_gp(route.vp, route.Tdp, route.DGp) * self.GS) * (self.t / route.tp)
        return bccq

    def __calculate_gp(self, vp, Tdp, DGp):
        """
        :return: Максимальное количество групп, которые могут пройти в сутки по однодневному участку туристского маршрута до его закрытия или до окончания светового дня, выражается целочисленным значением (единиц)
        """
        return 1 + int(vp * (self.Ts - Tdp) / DGp)


class TurObjAutonomous(TurObj):
    def __init__(self, name, Cfn, MC, Ts: float, GS: int, t: int, routes: List[OneDayTouristRouteWithTimeLim]):
        """
        :param name: название
        :param Cfn (list[float]): поправочные коэффициенты, которые учитывают определенные для туристских объектов лимитирующие факторы развития туризма (экологического, социального и социокультурного характера) и установленные режимы использования туристских объектов
        :param MC (float): коэффициент управленческой емкости, долей от единицы
        :param Ts: длина светового дня или количество времени, когда туристский маршрут доступен для посетителей, часов
        :param GS: среднее количество человек в группе (включая сопровождающих), человек
        :param t: количество дней в рассматриваемую единицу времени (месяц, сезон, год и др.), единиц
        :param routes: лист экземпляров однодневных маршрутов/участков
        """
        super().__init__(name, Cfn, MC)
        self.routes = routes
        self.Ts = Ts
        self.GS = GS
        self.t = t

    def __calculate_gp(self, vp, Tdp, DGp):
        """
        :return: Максимальное количество групп, которые могут пройти в сутки по однодневному участку туристского маршрута до его закрытия или до окончания светового дня, выражается целочисленным значением (единиц)
        """
        return 1 + int(vp * (self.Ts - Tdp) / DGp)

    def calculate_bccq(self):
        """
        :return: Базовая рекреационная емкость
        """
        gps = []
        for route in self.routes:
            gps.append(self.__calculate_gp(route.vp, route.Tdp, route.DGp))
        return min(gps) * self.GS * self.t
