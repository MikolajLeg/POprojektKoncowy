
from PyQt5.QtWidgets import QPushButton, QFileDialog, QTextEdit
from pdf_generator import PdfReportGenerator


# Class of buttons which are used to determine whether country should be included on map/chart
class CountryButton(QPushButton):
    def __init__(self, Country, update_method):
        super().__init__(Country.get_name())
        self.__country = Country
        self.__refresh_method = update_method
        # sets what will happen after clicking button
        self.clicked.connect(self.__status)
        self.__check_color()

# following method changes status of country associated with button,
    # this will later be used to determine if country should be included in map/chart or not
    def __status(self):
        self.__country.flip_status()
        # checks if button (country) is selected or not and applies color
        self.__check_color()
        # the following line refreshes the main window
        self.__refresh_method()

    def __check_color(self):
        # this method changes button color in order to show if country is selected or not
        if self.__country.get_status():
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: light gray")


# this button allows for choosing figure that should be displayed
class ChoiceButton(QPushButton):
    def __init__(self, name, set_method, check_method, update_method):
        super().__init__(name)
        self.__name = name
        # method used for sending feedback to main window
        self.__do_action_method = set_method
        self.__refresh_method = update_method
        self.__check_method = check_method
        self.clicked.connect(self.__choice)

    def __choice(self):
        self.__do_action_method(self.__name)
        self.check_color()
        # refreshing main window after setting what figure should be displayed
        self.__refresh_method()

    # method used for displaying correct color of button (yellow if selected, light gray if not)
    def check_color(self):
        if self.__check_method() == self.__name:
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: light gray")


# this class is serving as display, allowing to output errors(ErrorDisplay subclass)
# or information about selected country (CountryDisplay subclass)
class Display(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.LineWrapMode()
        self.adjustSize()
        self.setMaximumSize(575, 40)


class CountryDisplay(Display):
    def __init__(self):
        super().__init__()


class ErrorDisplay(Display):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("color: red")


# Button class that connects pdf generator
class PdfSaveButton(QPushButton):

    def __init__(self, name, update_error):
        super().__init__(name)
        # initializes PdfReportGenerator class which allows to create pdfs
        self.__pdf_generator = PdfReportGenerator()
        self.__chart = None
        self.__error_method = update_error
        self.__chart = None
        self.__data = None
        self.__start_date = None
        self.__end_date = None

        self.clicked.connect(self.__save_btn_action)

# updates data that will be used to create pdf
    def update_pdf_data(self, chart, start_date, end_date, data):
        self.__chart = chart
        self.__data = data
        self.__start_date = start_date
        self.__end_date = end_date

    # creates pdf with stored data, and saves it in chosen directory
    def __save_btn_action(self):
        filename = self.__prepare_file_chooser()
        # checks if directory, pdf will be saved to, have been chosen
        if filename:
            self.__pdf_generator.create_and_save_pdf(filename, self.__chart, self.__start_date,
                                                     self.__end_date, self.__data)
        else:
            self.__error_method("Save as PDF status: aborted")
            return

    # enables choice of directory pdf will be saved to
    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF report", filter="PDF ( *.pdf )")

        return filename
