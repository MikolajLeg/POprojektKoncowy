

from io import BytesIO
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from file_reader import DataGrinder


# class responsible for creating chart displaying energy prices
class ChartMaker(FigureCanvasQTAgg):

    def __init__(self, countries, start_date, end_date, disp):
        self.__maximum = 0
        self.__minimum = 1
        self.__dates = None
        self.__all_costs = dict()
        self.__start_date = start_date
        self.__end_date = end_date
        self.__countries = countries
        self.__lgd = list()
        self.__disp = disp
        self.__fig = Figure()
        self.__num_of_dates = 0

        super().__init__(self.__fig)
        self.__init_figure()

    # method responsible for initializing figure, clears it, sets tittle, and induces successive methods
    def __init_figure(self):
        self.__fig.clear()
        self.__fig.add_subplot()
        self.__fig.suptitle(f"Energy prices for Europe countries in years between "
                            f"{self.__start_date} - {self.__end_date}")
        self.__prepare_data()
        self.__make_chart()
        self.__fig.tight_layout()

    def __prepare_data(self):
        count = 0
        for country in self.__countries:
            count = count + 1
            # checks if limit of 6 countries to be on chart at singular time is met
            if count > 6:
                self.__disp.append("Error: Too many selected countries, only six are displayed")
                break
            Grinder = DataGrinder()
            dates, costs = Grinder.grind_data(self.__start_date, self.__end_date, country)

            for cost in costs:
                self.__check_min_max(cost)

            # put dates and corresponding values lists inside dictionary with country name serving as kay
            self.__lgd.append(country.get_name())
            self.__all_costs[country.get_name()] = costs
            if not self.__dates:
                self.__dates = dates
            self.__num_of_dates = len(dates)

    # method responsible for plotting selected countries on figure, as well as controlling x/y tick labels
    def __make_chart(self):
        ax = self.__fig.axes[0]

        for country in self.__all_costs.keys():
            ax.plot(self.__dates, self.__all_costs[country], "--*")
        self.__minimum = self.__minimum.__round__(2)
        self.__maximum = self.__maximum.__round__(2)

        # sets y ticks
        ax.set_yticks(np.arange(self.__minimum, self.__maximum, 0.05))

        if self.__num_of_dates > 12:
            frequency = np.ceil(self.__num_of_dates/12)
            tick_dates = self.__dates
            frequency = int(frequency)
            tick_dates = tick_dates[0:-1:frequency]

            ax.set_xticks(tick_dates)

        ax.set_xlabel("dates")
        ax.set_ylabel("energy costs")
        ax.grid()
        ax.legend(self.__lgd)

    # finds maximum/minimum cost value - > this will later be used when calculating y ticks
    def __check_min_max(self, cost):
        if not cost:
            return
        else:
            if cost < self.__minimum:
                self.__minimum = cost
            if cost > self.__maximum:
                self.__maximum = cost

    # returns chart as img in order to allow inserting it into pdf
    def get_img(self):
        img_data = BytesIO()
        self.__fig.savefig(img_data, format="png")
        seek_offset = 0
        img_data.seek(seek_offset)

        return img_data
