from PyQt5.QtWidgets import QPushButton, QFileDialog
from reportlab.lib.utils import ImageReader

from PDFSKURWESYNU import PdfReportGenerator


class PdfSaveButton(QPushButton):
    def __init__(self, name, chart):
        super().__init__(name)
        self.__chart = chart
        self.__pdf_generator = PdfReportGenerator()

        self.clicked.connect(self.__save_btn_action)

    

    def __save_btn_action(self):
        img_data = self.__chart.get_img()
        img = ImageReader(img_data)

        filename = self.__prepare_file_chooser()
        self.__pdf_generator.create_and_save_report(img, filename)

    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF report", filter="All Files (*)")
        return filename

