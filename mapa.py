

from translate import Translator
import geopandas as gpd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
#from shapely.geometry import Point


class MapMaker(FigureCanvasQTAgg):
    def __init__(self,countries,start_date,end_date,  width=10, height=15, dpi=100):
        self.__fig = Figure(figsize=(width, height), dpi=dpi)
        self.__list = countries
        self.__country_data = dict()
        self.__start_date = start_date
        self.__end_date = end_date
        self.__max_price = None
        self.__min_price = None
        super().__init__(self.__fig,)

        self.__init_map()


    def __init_map(self):
        self.__fig.suptitle(f"Ceny energii dla państw Unii Europejskiej w latach {self.__start_date} - {self.__end_date}")
        self.__ax = self.__fig.add_subplot(111)
        self.__data = gpd.read_file("NUTS_RG_60M_2021_3857_LEVL_0.geojson")

        self.__make_map()

    def __make_map(self):
        self.__ax.clear()
        self.__data.plot(ax =self.__ax,color="yellow", edgecolor="red",linewidth=0.4)
        self.__set_limits_on_axes()
        self.__prepare_countries()
        self.__check_countries()



    def __set_limits_on_axes(self):
        self.__ax.set_xlim([-3 * 1e6, 5.25 * 1e6])
        self.__ax.set_ylim([0.4 * 1e7, 1.2 * 1e7])

    def __prepare_countries(self):
        for country in self.__list:
            dates_and_costs = country.get_dates_and_cost()
            country_costs = 0
            num =0
            for k,v in dates_and_costs.items():
                if v == "no data":
                    continue
                else:
                    country_costs +=v
                    num +=1
            avg_cost = country_costs/num
            self.__price_check(avg_cost)

            self.__country_data[country.get_name()] = avg_cost


    def __check_countries(self):
        T = Translator()
        for country in self.__list:
            for nuts_name in self.__data.NAME_LATN:
                if "/" in nuts_name:
                    new_nuts_name = nuts_name.split("/")
                    new_nuts_name = new_nuts_name[1]
                else:
                    new_nuts_name = nuts_name

                new_nuts_name = T.translate(new_nuts_name)
                if new_nuts_name == country.get_name():
                    self.__paint_country(nuts_name,new_nuts_name)



    def __paint_country(self,nuts_name,country_name):
        self.__price_range()
        region = self.__data[self.__data.NAME_LATN == nuts_name]
        density = (self.__country_data[country_name] - self.__min_price)*self.__multi
        region.plot(ax=self.__ax, color=(density, 0.5,1 ))

    def __price_check(self,avg_cost):
        if not self.__max_price:
            self.__max_price = avg_cost
        if not self.__min_price:
            self.__min_price = avg_cost
        if self.__max_price < avg_cost:
            self.__max_price = avg_cost
        if self.__min_price > avg_cost:
            self.__min_price = avg_cost


    def __price_range(self):
        if self.__max_price == self.__min_price:
            self.__multi = 1%self.__max_price
        else:
            price_range = self.__max_price - self.__min_price
            self.__multi  = 1.0/price_range




