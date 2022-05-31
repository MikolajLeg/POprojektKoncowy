

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QVBoxLayout, QWidget, QSlider)


# noinspection PyUnresolvedReferences
class Slider(QWidget):
    def __init__(self, refresh_method, setting_start_date_method, setting_end_date_method, countries):
        super().__init__()
        self.__slider_1 = None
        self.__slider_2 = None
        # assigns methods that will allow us to send feedback signals to main window
        self.__refresh_method = refresh_method
        self.__setting_start_date = setting_start_date_method
        self.__setting_end_date = setting_end_date_method

        # We check if list of the provided countries is not empty, if it is we abort creating slider for now
        if len(countries) == 0:
            pass
        # if it is not empty we commence with creation of slider
        else:
            # we prepare a base list of dates which will allow us to "translate" positions of sliders
            # into dates via indexes
            data_1 = countries[1].get_dates_and_cost()
            data = list()
            for date in data_1.keys():
                data.append(date)

            self.__dates = data
            grid = QGridLayout()
            grid.addWidget(self.slider_features(), 2, 0)
            self.setLayout(grid)
            self.resize(200, 100)
            self.show()

    def slider_features(self):

        groupBox = QGroupBox()
        length = len(self.__dates)
        length = length-1

        # creates first slider which allows for setting start date
        self.__slider_1 = QSlider(Qt.Horizontal)
        self.__slider_1.valueChanged.connect(self.__set_start_date)
        self.__slider_1.setMinimum(0)
        self.__slider_1.setMaximum(length)

        # creates second slider which allows for setting end date
        self.__slider_2 = QSlider(Qt.Horizontal)
        self.__slider_2.valueChanged.connect(self.__set_end_date)
        self.__slider_2.setMinimum(1)
        self.__slider_2.setMaximum(length)
        self.__slider_2.setSliderPosition(length)
        self.__set_start_date()

        self.__slider_2.valueChanged.connect(self.value_check_2)
        self.__slider_1.valueChanged.connect(self.value_check_1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.__slider_1)
        vbox.addWidget(self.__slider_2)
        groupBox.setLayout(vbox)

        return groupBox

    # prevents slider 1 from going past slider 2
    def value_check_1(self):

        if self.__slider_1.sliderPosition() >= self.__slider_2.sliderPosition():
            self.__slider_2.setSliderPosition(self.__slider_1.sliderPosition() + 1)

    def value_check_2(self):

        if self.__slider_2.sliderPosition() <= self.__slider_1.sliderPosition():
            self.__slider_1.setSliderPosition(self.__slider_2.sliderPosition() - 1)

    # sets start date and refreshes main window with that new start date
    def __set_start_date(self):
        self.__setting_start_date(self.__dates[self.__slider_1.sliderPosition()])
        self.__refresh_method()

    # sets end date and refreshes main window with that new end date
    def __set_end_date(self):
        self.__setting_end_date(self.__dates[self.__slider_2.sliderPosition()])
        self.__refresh_method()
