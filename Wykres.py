

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ChartMaker(FigureCanvasQTAgg):

    def __init__(self, countries, start_date, end_date, disp):
        self.__maximum = 0
        self.__minimum = 1
        self.__all_dates = dict()
        self.__all_costs = dict()
        self.__start_date = start_date
        self.__end_date = end_date
        self.__countries = countries
        self.__lgd = list()
        self.__disp = disp
        # ustala pole self.__fig jako figure
        self.__fig = Figure()
        self.__num_of_dates = 0

        super().__init__(self.__fig)
        self.__init_figure()

    def __init_figure(self):
        # ustawia osie układu wspólrzęnych oraz tytuł dla stworzonej figury
        self.__fig.clear()
        self.__fig.add_subplot()
        self.__fig.suptitle(f"Ceny energii dla państw Unii Europejskiej w latach {self.__start_date} - {self.__end_date}")
        self.__prepare_data()
        self.__make_chart()
        self.__fig.tight_layout()

    def __make_chart(self):
        ax = self.__fig.axes[0]

        # rysuje wykres zależnosci cen od dat dla kolejnych państw
        for country in self.__all_dates.keys():
            ax.plot(self.__all_dates[country], self.__all_costs[country], "--*")
        self.__minimum = self.__minimum.__round__(2)
        self.__maximum = self.__maximum.__round__(2)

        # ustawia opis osi y (kosztow)
        ax.set_yticks(np.arange(self.__minimum, self.__maximum, 0.05))
        if self.__num_of_dates > 12:
            mulitiply = np.ceil(self.__num_of_dates/12)
            tick_dates = list()

            for dates in self.__all_dates.values():
                #print(self.__all_dates.values())
                if len(dates) < self.__num_of_dates:
                    continue
                else:
                    for num in range(len(dates)):

                        if num % mulitiply == 0:
                            tick_dates.append(dates[num])
                    break
            ax.set_xticks(tick_dates)

        ax.set_xlabel("data")
        ax.set_ylabel("koszt")
        ax.grid()
        ax.legend(self.__lgd)

    def __prepare_data(self):
        count = 0
        # tworzy listy cen dla kolejenych dat od początkowej do koncowej dla poszczególnych państw i wstawia do słownika
        for kraj in self.__countries:
            count = count + 1
            if count > 6:
                self.__disp.setText("Error: Zbyt dużo zanaznaczonych państw, wyswietlanie tylko czesci")
                break
            dates = list()
            costs = list()
            check = False

            if self.__start_date == self.__end_date:
                cost = kraj.get_dates_and_cost().get(self.__start_date)
                dates.append(self.__start_date)
                costs.append(cost)
                self.__check_min_max(cost)

            else:
                for date, cost in kraj.get_dates_and_cost().items():

                    if date == self.__start_date:
                        check = not check

                    if cost == 'no data':
                        dates.append(date)
                        costs.append(None)
                        continue

                    self.__check_min_max(cost)
                    if check:
                        dates.append(date)
                        costs.append(cost)

                    if date == self.__end_date:
                        check = not check

            self.__lgd.append(kraj.get_name())
            self.__all_dates[kraj.get_name()] = dates
            self.__all_costs[kraj.get_name()] = costs
            self.__num_of_dates = len(dates)

            if count < 7:
                self.__disp.clear()

    def __check_min_max(self, cost):
        if cost < self.__minimum:
            self.__minimum = cost
        if cost > self.__maximum:
            self.__maximum = cost
