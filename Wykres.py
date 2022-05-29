

from io import BytesIO
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from file_reader import DataGrinder


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
        self.__fig.suptitle(f"Ceny energii dla państw Europy w latach {self.__start_date} - {self.__end_date}")
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

                self.__disp.append("Error: Zbyt dużo zanaznaczonych państw, wyswietlanie tylko czesci")
                break
            Grinder = DataGrinder()
            dates, costs = Grinder.grind_data(self.__start_date,self.__end_date,kraj)

            for cost in costs:
                self.__check_min_max(cost)

            self.__lgd.append(kraj.get_name())
            self.__all_dates[kraj.get_name()] = dates
            self.__all_costs[kraj.get_name()] = costs
            self.__num_of_dates = len(dates)

    def __check_min_max(self, cost):
        if cost == None:
            return
        else:
            if cost < self.__minimum:
                self.__minimum = cost
            if cost > self.__maximum:
                self.__maximum = cost

    def get_img(self):
        img_data = BytesIO()
        self.__fig.savefig(img_data)
        seek_offset = 0
        img_data.seek(seek_offset)

        return img_data
