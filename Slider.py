
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox,
                             QVBoxLayout, QWidget, QSlider)

class Slider(QWidget):
    def __init__(self, lista):
        super().__init__()

        if len(lista) == 0:
            pass
        else:

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

        self.slider_1 = QSlider(Qt.Horizontal)
        self.slider_1.valueChanged.connect(lambda value: print(value))
        self.slider_1.setMinimum(0)
        self.slider_1.setMaximum(length)

        self.slider_2 = QSlider(Qt.Horizontal)
        self.slider_2.valueChanged.connect(lambda value: print(value))
        self.slider_2.setMinimum(0)
        self.slider_2.setMaximum(length)
        self.slider_2.setSliderPosition(length)

        self.slider_2.valueChanged.connect(self.ValueCheck)
        self.slider_1.valueChanged.connect(self.ValueCheck)


        vbox = QVBoxLayout()
        vbox.addWidget(self.slider_1)
        vbox.addWidget(self.slider_2)
        groupBox.setLayout(vbox)

        return groupBox


    def ValueCheck(self):

        if self.slider_1.sliderPosition() > self.slider_2.sliderPosition():
            self.slider_2.setSliderPosition(self.slider_1.sliderPosition())


# app = QApplication([])
# window = Slider()
# window.show()
# app.exec_()
