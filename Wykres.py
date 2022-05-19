

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class Rysuj(FigureCanvasQTAgg):

    def __init__(self, kraje, start_date, end_date,disp):
        # ustala pole self.__fig jako figure
        self.__disp = disp
        self.__fig = Figure()
        super().__init__(self.__fig)
        self.__init_figure(kraje, start_date, end_date)
        self.__maximum = 0
        self.__minimum = 1


    def __init_figure(self, Kraje, start_date, end_date):
        # ustawia osie układu wspólrzęnych oraz tytuł dla stworzonej figury
        self.__fig.clear()
        self.__fig.add_subplot()
        self.__fig.suptitle(f"Ceney energii dla państw Unii Europejskiej w latach {start_date} - {end_date}")
        self.__wykres(Kraje, start_date, end_date)
        self.__fig.tight_layout()

    def __wykres(self, Kraje, start_date, end_date):
        alldates = dict()
        allcosts = dict()
        lgd = list()
        minimum = 1
        maximum = 0
        ax = self.__fig.axes[0]
        count = 0
        # tworzy listy cen dla koljenych dat od początkowej do koncowej dla poszczególnych państw i wstawia do słownika
        for kraj in Kraje:
            count = count +1
            if count > 6:
                self.__disp.setText("Error: Zbyt dużo zanaznaczonych państw, wyswietlanie tylko czesci")
                break
            dates = list()
            costs = list()
            check = False
            for date, cost in kraj.get_dates_and_cost().items():
                if start_date == end_date:
                    if start_date == date:
                        dates.append(date)
                        costs.append(cost)
                        if cost < minimum:
                            minimum = cost
                        if cost > maximum:
                            maximum = cost
                        break
                    else:
                        continue
                else:
                    if date == start_date:
                        check = not check

                    if cost == 'no data':
                        dates.append(date)
                        costs.append(None)
                        continue
                    if cost < minimum:
                        minimum = cost
                    if cost > maximum:
                        maximum = cost

                    if check:
                        dates.append(date)
                        costs.append(cost)

                    if date == end_date:
                        check = not check

            lgd.append(kraj.get_name())

            alldates[kraj.get_name()] = dates
            allcosts[kraj.get_name()] = costs



        # rysuje wykres zależnosci cen od dat dla kolejnych państw
        for kraj in alldates.keys():
            ax.plot(alldates[kraj], allcosts[kraj], "--*")
        minimum = minimum.__round__(2)
        maximum = maximum.__round__(2)

        if count <7 :
            self.__disp.clear()

        ax.set_yticks(np.arange(minimum,maximum, 0.05))
        ax.set_xlabel("data")
        ax.set_ylabel("koszt")
        ax.grid()
        ax.legend(lgd)

    def check_min_max(self, cost):

        if cost < self.__minimum:
            self.__minimum = cost
        if cost > self.__maximum:
            self.__maximum = cost




