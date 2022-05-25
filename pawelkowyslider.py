import sys
import geopandas as gpd

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QVBoxLayout, QGridLayout
from PyQt5.Qt import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from shapely.geometry import Point


class MapChart(FigureCanvasQTAgg):
    def __init__(self, path_to_region_geojson, width=10, height=15, dpi=100):
        self.__fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.__fig)

        self.__path_to_region_geojson = path_to_region_geojson

        self.__init_view()

    def update_with_values(self, values):
        print(values)
        self.__color_fill = (values[0] % 255 / 255.0, values[0] % 128 / 100.0, values[1] % 128 / 100.0 ) # TODO
        self.__update_plot()

    def __init_view(self):
        self.__ax = self.__fig.add_subplot(111)
        self.__selected = None
        self.__color_fill = "blue"
        self.__plot_data()
        self.__add_mouse_listener()

    def __plot_data(self):
        self.__region_df = gpd.read_file(self.__path_to_region_geojson)
        self.__update_plot()

    def __update_plot(self):
        self.__ax.clear()
        self.__region_df.plot(ax=self.__ax, color="yellow", edgecolor="red", linewidth=0.3)
        selected = self.__selected

        if selected is not None:
            region = self.__region_df[self.__region_df.CNTR_CODE == selected]
            region.plot(ax=self.__ax, color=self.__color_fill)

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
                self.__selected = name
                self.__update_plot()


class DoubleSlider(QWidget):

    def __init__(self, width_height, update_callback, parent=None, min_val=0, max_val=100):
        super().__init__(parent)
        self.__validate_args(min_val, max_val)

        self.__min_val = min_val
        self.__max_val = max_val

        self.__width_height = width_height
        self.__update_callback = update_callback

        self.__create_view()

    def get_values(self):
        values = self.__top_slider.value(), self.__bottom_slider.value()
        return values

    def __validate_args(self, min_val, max_val):
        if min_val >= max_val:
            raise Exception("Incorrect initial value of DoubleSlider (max_val cannot be lower or equal to min_val).")


    def __create_view(self):
        self.__top_slider = self.__create_top_slider()
        self.__bottom_slider = self.__create_bottom_slider()

        layout = QVBoxLayout()
        layout.addWidget(self.__top_slider)
        layout.addWidget(self.__bottom_slider)

        self.setMinimumWidth(self.__width_height)
        self.setMaximumWidth(self.__width_height)
        self.setMaximumHeight(self.__width_height)

        self.setLayout(layout)


    def __create_top_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(self.__min_val)
        slider.setMaximum(self.__max_val - 1)

        slider.setValue(self.__min_val)
        slider.valueChanged.connect(self.__handle_top_change)

        return slider

    def __create_bottom_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(self.__min_val + 1)
        slider.setMaximum(self.__max_val)

        slider.setValue(self.__max_val)
        slider.valueChanged.connect(self.__handle_bottom_change)

        return slider

    def __handle_top_change(self):
        left_value = self.__top_slider.value()
        right_value = self.__bottom_slider.value()

        if left_value >= right_value:
            self.__bottom_slider.setValue(left_value + 1)

        self.__update_callback()


    def __handle_bottom_change(self):
        left_value = self.__top_slider.value()
        right_value = self.__bottom_slider.value()

        if right_value <= left_value:
            self.__top_slider.setValue(right_value - 1)

        self.__update_callback()



class SliderApp(QMainWindow):

    def __init__(self, path_to_nuts_data, parent=None):
        super().__init__(parent)
        self.__path_to_nuts_data = path_to_nuts_data

        self.__init_default_value()
        self.__init_view()

        self.show()

    def __init_default_value(self):
        self.__padding_x = 400
        self.__padding_y = 400
        self.__width = 960
        self.__height = 600

    def __init_view(self):
        self.setWindowTitle("SliderApp example")
        self.setGeometry(self.__padding_x, self.__padding_y, self.__width, self.__height)

        main_layout = QGridLayout()
        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        self.__add_widgets_to_main_layout(main_layout)

        self.setCentralWidget(main_widget)

    def __add_widgets_to_main_layout(self, main_layout):
        slider_width_height = self.__width // 4

        self.__chart_widget = MapChart(self.__path_to_nuts_data)
        self.__double_slider_widget = DoubleSlider(slider_width_height, self.__update_on_click)

        main_layout.addWidget(self.__chart_widget, 0, 0)
        main_layout.addWidget(self.__double_slider_widget, 0, 1)

    def __update_on_click(self):
         values = self.__double_slider_widget.get_values()
         self.__chart_widget.update_with_values(values)


def main(path_to_nuts_data):
    app = QApplication([])

    slider_app = SliderApp(path_to_nuts_data)

    sys.exit(app.exec_())


if __name__ == "__main__":
    path_to_data = "./NUTS_RG_60M_2021_3857_LEVL_0.geojson"

    main(path_to_data)
