
class Czytnik:

    def __init__(self):
        self.__data = dict()

    def read_file(self, filepath):
        with open(filepath, "r") as file:
            self.__all_lines = file.readlines()[0:]
            # czyta plik 
            # przyporządkowuje pierwszą linijkę(z datami) do zmiennej daty za pomoca metody prepare_dates
            self.__prepare_dates()

            # bierze linijki z danymi dla państw Unii
            lines = self.__all_lines[4:]
            for line in lines:
                # zamienia przecinki wewnątrz cen na kropki
                dotcomma = False
                for i in range(0, len(line)):
                    if line[i] == '"':
                        dotcomma = not dotcomma
                    if line[i] == ",":
                        if dotcomma:
                            line = line[:i] + '.' + line[i+1:]

                line = line.rstrip("\n")
                # pozbywa się niepotrzebnych cudzysłowów
                line = line.replace('"', "")
                line = line.replace(':', 'no data')

                # rozdziela linijke na kolejne ceny na podstawie zewnętrznych przecinków
                line = line.split(',')
                name = line[0]
                name = name.split("(")
                name = name[0]

                price = list()
                # upakowuje kolejne ceny w wybranej linii(dla danego państwa) do listy
                for i in range(1, len(line)):
                    if line[i] == "no data":
                        price.append(line[i])
                    else:
                        price.append(float(line[i]))

                # ceny enrgii dla danego państwa przyporządkowuje odpowiednim data i wkłada do słownika z nazwą
                # państwa jako kluczem
                count = 1
                self.__data[name] = dict()
                for p in price:
                    # print(count,end="- ")
                    datetime = self.__dates[count]
                    # print(datetime, end= "- ")
                    # print(p)
                    self.__data[name][datetime] = p
                    count += 1



        return self.__data

    def __prepare_dates(self):
        self.__dates = self.__all_lines[0]
        # pozbywa się znaku \n z końca linijki
        self.__dates = self.__dates.rstrip("\n")
        # rozdziela linikje na poszczególne daty
        self.__dates = self.__dates.split(",")


class DataGrinder:
    def __init__(self):
        pass

    def grind_data(self,start_date,end_date, country):
        dates = list()
        costs = list()
        check = False

        if start_date == end_date:
            cost = country.get_dates_and_cost().get(start_date)
            dates.append(start_date)
            costs.append(cost)

        else:
            for date, cost in country.get_dates_and_cost().items():

                if date == start_date:
                    check = not check

                if check:
                    if cost == 'no data':
                        dates.append(date)
                        costs.append(None)
                        continue
                    else:
                        dates.append(date)
                        costs.append(cost)

                if date == end_date:
                    check = not check


        return dates, costs
