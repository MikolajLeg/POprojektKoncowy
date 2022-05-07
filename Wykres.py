import numpy as np
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class Rysuj(FigureCanvasQTAgg):

    def __init__(self, Kraje, start_date, end_date):
        #ustala pole self.__fig jako figure
        self.__fig = Figure()
        super().__init__(self.__fig)
        self.__init_figure(Kraje,start_date,end_date)


    def __init_figure(self,Kraje,start_date,end_date):
        #ustawia osie układu wspólrzęnych oraz tytuł dla stworzonej figury
        self.__fig.add_subplot()
        self.__fig.suptitle(f"Ceney energii dla państw Unii Europejskiej w latach {start_date} - {end_date}")
        self.wykres(Kraje,start_date,end_date)
        self.__fig.tight_layout()



    def wykres(self,Kraje,start_date,end_date):
        alldates = dict()
        allcosts = dict()
        lgd =list()
        minimum = 1
        maximum = 0
        ax = self.__fig.axes[0]
        # tworzy listy cen dla koljenych dat od początkowej do koncowej dla poszczególnych państw i wstawia do słownika
        for kraj in Kraje:
            dates = list()
            costs = list()
            check = False
            for date,cost in kraj.get_dates_and_cost().items():
                if date == start_date:
                    check = not check
                elif date == end_date:
                    check = not check
                if cost == 'no data':
                    continue
                if cost < minimum:
                    minimum = cost
                if cost > maximum :
                    maximum = cost

                if check == True:
                    dates.append(date)
                    costs.append(cost)

            lgd.append(kraj.get_name())

            alldates[kraj] =dates
            allcosts[kraj] = costs

        # rysuje wykres zależnosci cen od dat dla kolejnych państw
        for kraj in Kraje:
            ax.plot(alldates[kraj],allcosts[kraj])
        minimum = minimum.__round__(2)
        maximum = maximum.__round__(2)

        ax.set_yticks(np.arange(minimum,maximum,0.1))
        ax.set_xlabel("data")
        ax.set_ylabel("koszt")
        ax.grid()
        ax.legend(lgd)
