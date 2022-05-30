

from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from file_reader import DataGrinder



class PdfReportGenerator:

    def __init__(self):
        self.__title =  "pdf"
        self.__country_list = list()
        self.__dates_and_prices_list = list()
        self.__dictionary = dict()


    def create_and_save_pdf(self,filepath, chart, start_date, end_date, countries, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, chart, start_date, end_date, countries, pagesize)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, chart,start_date,end_date, countries, pagesize):

        self.__get_data(start_date, end_date, countries)
        img = self.__turn_chart_to_img(chart)
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Times-Roman",20)
        title = " Analiza cen energii w panstwach Europy"
        title_offset, img_offset, data_offset = 50, 550, 1200
        title_x, title_y = A4[0] / 2, A4[1] - title_offset
        chart_x, chart_y = 0, A4[1] - img_offset
        data_x, data_y =  30, A4[1] - img_offset

        canvas.drawCentredString(title_x, title_y, title)
        canvas.drawImage(img,chart_x,chart_y, 600, 450)
        print("drawstring")
        i = 0
        # self.t.wrapOn(canvas, 2, 2)
        # self.t.drawOn(canvas, 2, 2)

        textobject = canvas.beginText(data_x,data_y)
        num_of_page = 0
        #textobject.setTextOrigin(data_x, data_y)
        textobject.setFont("Times-Roman",20)

        count = 0
        for country in self.__dictionary.keys():
            count += 1
            if count > 6:
                break
            textobject.textLine(" ")
            textobject.textLine(country)
            for d,c in self.__dictionary[country].items():
                c = str(c)
                if c == None:
                    text = d + " None"
                else:
                    text = f" date: {d:<8}  | cost:  {c:<10} "

                textobject.textLine(text)

                if textobject.getY() < 0:
                    textobject.setTextOrigin(data_x, data_y)
                    canvas.drawText(textobject)
                    # textobject = None
                    num_of_page += 1
                    canvas.showPage()
                    data_y = A4[1] -25
                    textobject = canvas.beginText(data_x,data_y)
                    textobject.setFont("Times-Roman", 20)

        textobject.setTextOrigin(data_x, data_y)
        canvas.drawText(textobject)

        # canvas.showPage()

        #canvas.drawString(self.__tab, data_x, data_y)
        #canvas.drawString(self.t,data_x, data_y)

        return canvas

    def __turn_chart_to_img(self, chart):

        img_data = chart.get_img()
        img = ImageReader(img_data)

        return img

    def __get_data(self,start_date,end_date, countries):
        Grinder = DataGrinder()

        for country in countries:
            country_dict = dict()
            dates, costs = Grinder.grind_data(start_date,end_date,country)
            index = 0
            for d in dates:
                country_dict[d] = costs[index]
                index +=1
            self.__dictionary[country.get_name()] = country_dict








        # for country in countries:
        #     self.__country_list.append(country.get_name())
        #     for d, price in country.get_dates_and_cost().items():
        #         l = list()
        #         l.append(d)
        #         l.append(price)
        #         self.__dates_and_prices_list.append(l)



