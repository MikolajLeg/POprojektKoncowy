
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from file_reader import DataGrinder


# class responsible for creating pdf-s basing on provided data
class PdfReportGenerator:

    def __init__(self):
        self.__title = "pdf"
        self.__country_list = list()
        self.__dates_and_prices_list = list()
        self.__dictionary = dict()

    # method responsible for initializing other methods and saving pdf to selected file
    def create_and_save_pdf(self, filepath, chart, start_date, end_date, countries, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, chart, start_date, end_date, countries, pagesize)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    # method responsible for creating pdf template with last used chart as img,
    # and data used for that chart presented in columns below
    def __create_pdf_template(self, filepath, chart, start_date, end_date, countries, pagesize):

        self.__get_data(start_date, end_date, countries)
        self.__turn_chart_to_img(chart)
        # creates canvas and sets some of its basic properties
        # (tittle/font/offsets of img/data that will be later placed in pdf)
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Times-Roman", 20)
        title = " Analysis of energy prices in Europe countries"
        title_offset, img_offset, data_offset = 50, 550, 1200
        title_x, title_y = A4[0] / 2, A4[1] - title_offset
        chart_x, chart_y = 0, A4[1] - img_offset
        data_x, data_y = 30, A4[1] - img_offset

        # puts chart as img and tittle on canvas
        canvas.drawCentredString(title_x, title_y, title)
        canvas.drawImage(self.__img, chart_x, chart_y, 600, 450)

        text_object = canvas.beginText(data_x, data_y)
        text_object.setFont("Times-Roman", 20)
        count = 0

        # write dates and corresponding to them values for each pictured on chart country in pdf
        for country in self.__dictionary.keys():
            count += 1
            if count > 6:
                break
            text_object.textLine(" ")
            text_object.textLine(country)
            for d, c in self.__dictionary[country].items():
                c = str(c)
                if not c:
                    text = d + " None"
                else:
                    text = f" date: {d:<8}  | cost:  {c:<10} "

                text_object.textLine(text)

                # if length of text lines exceeds length of page, lines that are already prepared are written down
                # and then a new page is added where following lines will be written
                if text_object.getY() < 0:
                    text_object.setTextOrigin(data_x, data_y)
                    canvas.drawText(text_object)
                    canvas.showPage()
                    data_y = A4[1] - 25
                    text_object = canvas.beginText(data_x, data_y)
                    text_object.setFont("Times-Roman", 20)

        canvas.drawText(text_object)

        return canvas

    def __turn_chart_to_img(self, chart):
        img_data = chart.get_img()
        self.__img = ImageReader(img_data)

    # prepares data that will later be used while creating pdf
    def __get_data(self, start_date, end_date, countries):
        Grinder = DataGrinder()

        for country in countries:
            country_dict = dict()
            dates, costs = Grinder.grind_data(start_date, end_date, country)
            index = 0
            for d in dates:
                country_dict[d] = costs[index]
                index += 1
            self.__dictionary[country.get_name()] = country_dict
