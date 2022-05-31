

from translate import Translator
import geopandas as gpd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from shapely.geometry import Point


# class responsible for creating map of countries
class MapMaker(FigureCanvasQTAgg):
    def __init__(self, countries, start_date, end_date, error_display, display,  width=10, height=15, dpi=100):
        self.__fig = Figure(figsize=(width, height), dpi=dpi)
        self.__list = countries
        self.__country_data = dict()
        self.__start_date = start_date
        self.__end_date = end_date
        self.__max_price = None
        self.__min_price = None
        self.__error_disp = error_display
        self.__display = display

        super().__init__(self.__fig)
        self.__init_map()

    # method responsible for initializing view of map
    def __init_map(self):
        # setting map tittle, adding axes and map data
        self.__fig.suptitle(f"Energy prices for Europe countries in years between"
                            f" {self.__start_date} - {self.__end_date}")
        self.__ax = self.__fig.add_subplot(111)
        self.__data = gpd.read_file("NUTS_RG_60M_2021_3857_LEVL_0.geojson")

        self.__make_map()
        self.__add_mouse_listener()

    # method responsible for plotting basic map (with all countries colored grey)
    def __make_map(self):
        self.__ax.clear()
        self.__data.plot(ax=self.__ax, color="lightgrey", edgecolor="red", linewidth=0.4)

        self.__set_limits_on_axes()
        self.__prepare_countries()
        self.__check_countries()

    # sets ax limit since full map is unnecessary big
    def __set_limits_on_axes(self):
        self.__ax.set_xlim([-3 * 1e6, 5.25 * 1e6])
        self.__ax.set_ylim([0.4 * 1e7, 1.2 * 1e7])

    # prepares data about countries (avg_price for countries)
    def __prepare_countries(self):
        for country in self.__list:
            country_costs = 0
            num = 0
            dates_and_costs = country.get_dates_and_cost()
            check = False

            if self.__start_date == self.__end_date:
                if dates_and_costs[self.__start_date] == 'no data':
                    country_costs = 0
                else:
                    num += 1
                    country_costs = dates_and_costs[self.__start_date]

            else:
                for date, cost in dates_and_costs.items():
                    if date == self.__start_date:
                        check = not check
                    if cost == 'no data':
                        continue
                    if check:
                        country_costs += cost
                        num += 1
                    if date == self.__end_date:
                        check = not check

            if num == 0:
                num = 1

            avg_cost = country_costs/num
            avg_cost = round(avg_cost, 3)
            self.__price_check(avg_cost)
            self.__country_data[country.get_name()] = avg_cost

    # method responsible for finding and initialing painting method of selected countries
    def __check_countries(self):
        T = Translator()
        for country in self.__list:
            if country.get_status():
                for nuts_name in self.__data.NAME_LATN:
                    if "/" in nuts_name:
                        new_nuts_name = nuts_name.split("/")
                        new_nuts_name = new_nuts_name[1]
                    else:
                        new_nuts_name = nuts_name

                    new_nuts_name = T.translate(new_nuts_name)
                    if new_nuts_name == country.get_name():
                        self.__paint_country(nuts_name, new_nuts_name)

    # paints selected country
    def __paint_country(self, nuts_name, country_name):
        self.__price_range()
        region = self.__data[self.__data.NAME_LATN == nuts_name]
        density = (self.__country_data[country_name] - self.__min_price)*self.__multi
        region.plot(ax=self.__ax, color=(1-density, 1-density, 1), legend=True)

    # finds maximum and minimum price
    def __price_check(self, avg_cost):
        if not self.__max_price:
            self.__max_price = avg_cost
        if not self.__min_price:
            self.__min_price = avg_cost
        if self.__max_price < avg_cost:
            self.__max_price = avg_cost
        if self.__min_price > avg_cost:
            self.__min_price = avg_cost

# checks price range of prices and creates multiplier that will later be used to determine country color intensity
    def __price_range(self):

        if self.__max_price == self.__min_price:
            if self.__max_price == 0:
                self.__multi = 0
            else:
                self.__multi = 1 % self.__max_price
        else:
            price_range = self.__max_price - self.__min_price
            self.__multi = 1.0 / price_range

    # add mouse listener
    def __add_mouse_listener(self):
        self.__fig.canvas.mpl_connect("button_press_event", self.__check_click__coordinates)

    # check coordinates of click, determining what country have been selected
    def __check_click__coordinates(self, event):
        coordinates = event.xdata, event.ydata
        current_point = Point(coordinates)

        for name, points in zip(self.__data.NAME_LATN, self.__data.geometry):
            if points.contains(current_point):
                T = Translator()
                if "/" in name:
                    name = name.split("/")
                    name = name[1]
                name = T.translate(name)
                # displays information about average price of energy in selected country during selected period
                if name in self.__country_data.keys():
                    self.__display.append(f"{name} : {self.__country_data[name]} ")
                    return
                elif name == "Switzerland":
                    self.__error_disp.append("It's not a bug, it's a feature")
                    return
                else:
                    return

        self.__error_disp.append("out of bounds")
