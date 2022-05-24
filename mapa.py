import fiona
import shapely
import pyproj
import rtree
import geopandas as gpd
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from shapely.geometry import Point
import geopandas






# DATA SOURCE: https://gisco-services.ec.europa.eu/distribution/v2/nuts/download/ref-nuts-2021-60m.geojson.zip
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from shapely.geometry import Point
from PyQt5.QtCore import Qt


class MapChart(FigureCanvasQTAgg):
    def __init__(self, path_to_region_geojson, width=10, height=15, dpi=100):
        self.__fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.__fig)

        self.__path_to_region_geojson = path_to_region_geojson

        self.__init_view()



    def __init_view(self):
        self.__ax = self.__fig.add_subplot(111)
        self.__plot_data()
        self.__add_mouse_listener()

    def __plot_data(self):
        self.__region_df = gpd.read_file(self.__path_to_region_geojson)
        self.__update_plot()

    def __update_plot(self, selected=None):
        self.__ax.clear()
        self.__region_df.plot(ax=self.__ax, color="grey", edgecolor="red", linewidth=0.3)

        if selected is not None:
            region = self.__region_df[self.__region_df.CNTR_CODE == selected]
            region.plot(ax=self.__ax, color="blue")

        self.__set_axis_lim()
        self.__fig.canvas.draw()

    def __set_axis_lim(self):
        self.__stdout_red("Warning! Setting axis lim!")
        self.__ax.set_xlim([-3 * 1e6, 6 * 1e6])
        self.__ax.set_ylim([0.25 * 1e7, 1.2 * 1e7])

    def __stdout_red(self, message):
        red_start = "\033[91m"
        red_end = "\033[0m"
        print(f"{red_start}{message}{red_end}")

    def __add_mouse_listener(self):
        self.__fig.canvas.mpl_connect("button_press_event", self.__check_coords_on_click)

    def __check_coords_on_click(self, event):
        coords = event.xdata, event.ydata
        current_point = Point(coords)

        for name, points in zip(self.__region_df.CNTR_CODE, self.__region_df.geometry):
            if points.contains(current_point):
                print("Clicked: ", name)
                self.__update_plot(name)



class MapApp(QMainWindow):

    def __init__(self, path_to_nuts_data, lista, window, parent=None):
        super().__init__(parent)

        if len(lista) == 0:
            pass
        else:
            self.__window = window
            costs_1 = lista[1].get_dates_and_cost()
            costs = list()
            for cost in costs_1.keys():
                costs.append(cost)



        self.__path_to_nuts_data = path_to_nuts_data

        self.__init_default_value()
        self.__init_view()

        self.show()

    def __init_default_value(self):
        self.__padding_x = 400
        self.__padding_y = 400
        self.__width = 800
        self.__height = 600

    def __init_view(self):
        self.setWindowTitle("GeoPandas example")
        self.setGeometry(self.__padding_x, self.__padding_y, self.__width, self.__height)

        self.__create_chart()

    # def __create_chart(self):
    #     chart_widget = MapChart(self.__path_to_nuts_data, )
    #     self.setCentralWidget(chart_widget)




if __name__ == "__main__":
    app = QApplication([])
    path_to_data = "./NUTS_RG_60M_2021_3857_LEVL_0.geojson"

    mapApp = MapApp(path_to_data)

    sys.exit(app.exec_())
