

import geopandas as gpd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
#from shapely.geometry import Point




class MapMaker(FigureCanvasQTAgg):
    def __init__(self,countries):
        self.__fig = Figure()
        self.__list = countries
        self.__country_data = dict()
        super().__init__(self.__fig)

        self.__init_map()


    def __init_map(self):
        self.__ax = self.__fig.add_subplot(111)
        self.__data = gpd.read_file("NUTS_RG_60M_2021_3857_LEVL_0.geojson")

        self.__make_map()

    def __make_map(self):
        self.__ax.clear()
        self.__data.plot(ax =self.__ax,color="yellow", edgecolor="red",linewidth=0.4)
        self.__set_limits_on_axes()
        self.__check_countries()


    def __set_limits_on_axes(self):
        self.__ax.set_xlim([-3 * 1e6, 5.25 * 1e6])
        self.__ax.set_ylim([0.4 * 1e7, 1.2 * 1e7])

    def __prepare_countries(self):
        for country in self.__list:
            dates_and_costs = country.get_dates_and_costs()
            for k,v in dates_and_costs
            self.__country_data[country.get_name()]


    def __check_countries(self):
        for country in self.__list:
            for nuts_name in self.__data.NAME_LATN:
                 if "/" in nuts_name:
                      new_nuts_name = nuts_name.split("/")
                      new_nuts_name = new_nuts_name[1]
                 else:
                     new_nuts_name =nuts_name

                 if new_nuts_name == country.get_name():
                     print(" ")
                     print("THEY ARE SAME")
                     print(nuts_name)
                     print(country.get_name())
                     self.__paint_country(nuts_name)

    def __paint_country(self,nuts_name):
        region = self.__data[self.__data.NAME_LATN == nuts_name]
        region.plot(ax=self.__ax, color="blue" ,))


