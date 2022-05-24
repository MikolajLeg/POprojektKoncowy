from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys

  
# class for scrollable label
class ScrollLabel(QScrollArea):
  
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
  
        # making widget resizable
        self.setWidgetResizable(True)
  
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
  
        # vertical box layout
        lay = QVBoxLayout(content)
  
        # creating label
        self.label = QLabel(content)
  
        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)

    # getting text method
    def text(self):

        # getting text of the label
        get_text = self.label.text()

        # return the text
        return get_text


