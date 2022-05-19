from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import ( QGridLayout, QGroupBox,
                             QVBoxLayout, QWidget, QSlider)

class Slider(QWidget):
    def __init__(self,Okno, lista):
        super().__init__()

        if len(lista) == 0:
            pass
        else:
            self.__okno = Okno
            data_1 = lista[1].get_dates_and_cost()
            data = list()
            for date in data_1.keys():
                data.append(date)

            self.dates = data
            grid = QGridLayout()
            grid.addWidget(self.SliderFeatures(), 2, 0)
            self.setLayout(grid)
            self.resize(200, 100)
            self.show()

    def SliderFeatures(self):

        groupBox = QGroupBox()
        length = len(self.dates)
        length = length-1


        self.slider_1 = QSlider(Qt.Horizontal)
        self.slider_1.valueChanged.connect(self.__set_start_date)
        self.slider_1.setMinimum(0)
        self.slider_1.setMaximum(length)

        self.slider_2 = QSlider(Qt.Horizontal)
        self.slider_2.valueChanged.connect(self.__set_end_date)
        self.slider_2.setMinimum(0)
        self.slider_2.setMaximum(length)
        self.slider_2.setSliderPosition(length)
        self.__set_start_date()

        self.slider_2.valueChanged.connect(self.ValueCheck_2)
        self.slider_1.valueChanged.connect(self.ValueCheck_1)


        vbox = QVBoxLayout()
        vbox.addWidget(self.slider_1)
        vbox.addWidget(self.slider_2)
        groupBox.setLayout(vbox)

        return groupBox


    def ValueCheck_1(self):

        if self.slider_1.sliderPosition() > self.slider_2.sliderPosition():
            self.slider_2.setSliderPosition(self.slider_1.sliderPosition())

    def ValueCheck_2(self):

        if self.slider_2.sliderPosition() < self.slider_1.sliderPosition():
            self.slider_1.setSliderPosition(self.slider_2.sliderPosition())


    def __set_start_date(self):
        self.__okno.set_start_date(self.dates[self.slider_1.sliderPosition()])
        self.__okno.refresh_view()

    def __set_end_date(self):
        self.__okno.set_end_date(self.dates[self.slider_2.sliderPosition()])
        self.__okno.refresh_view()

