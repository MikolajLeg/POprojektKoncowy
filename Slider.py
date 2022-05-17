import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)

class Slider(QWidget):
    def __init__(self, start_date, edn_date):
        super().__init__()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(lambda value: print(value))


