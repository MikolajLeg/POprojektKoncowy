from PyQt5.Qt import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QSlider, QHBoxLayout, QLabel, \
    QTextEdit


class SliderElem(QHBoxLayout):
    def __init__(self, name, min_value, max_value, init_value, update_callback, width=100, height=30):
        super().__init__()

        self.__name = name
        self.__min_value = min_value
        self.__max_value = max_value
        self.__init_value = init_value
        self.__update_callback = update_callback
        self.__width = width
        self.__height = height

        self.__create_all()

    def get_value(self):
        return self.__slider.value()

    def __create_all(self):
        self.__label = self.__create_label()
        self.__slider = self.__create_slider()
        current_value = self.__slider.value()
        self.__value_text_box = self.__create_value_text_box(current_value)

        self.addWidget(self.__label)
        self.addWidget(self.__slider)
        self.addWidget(self.__value_text_box)
        self.setAlignment(Qt.AlignLeft)

    def __create_label(self, width=50):
        label = QLabel(self.__name)
        label.setMinimumWidth(width)
        label.setMaximumWidth(width)

        return label

    def __create_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(self.__min_value)
        slider.setMaximum(self.__max_value)
        slider.setValue(self.__init_value)

        slider.setMinimumSize(self.__width, self.__height)
        slider.setMaximumSize(self.__width, self.__height)

        slider.valueChanged.connect(self.__update_callback)
        slider.valueChanged.connect(self.__update_text_box)

        return slider

    def __create_value_text_box(self, initial_value, width=50):
        value_text_box = QTextEdit(str(initial_value))
        value_text_box.setReadOnly(True)

        height = QFontMetrics(value_text_box.font()).lineSpacing() * 2
        value_text_box.setFixedHeight(height)

        value_text_box.setMinimumWidth(width)

        return value_text_box

    def __update_text_box(self):
        current_value = self.__slider.value()
        value2str = str(current_value)
        self.__value_text_box.setText(value2str)
