
class Czytnik:

    def __init__(self):
        pass

    def read_file(self,filepath):
        with open(filepath, "r") as file:
            data = dict()
            alllines = file.readlines()[0:]
            # czyta plik po czym czym przyporządkowuje pierwszą linijkę(z datami) do zmiennej daty
            dates = alllines[0]
            # pozbywa się znaku \n z końca linijki
            dates = dates.rstrip("\n")
            # rozdziela linikje na poszczególne daty
            dates = dates.split(",")

            # bierze linijki z danymi dla państw Unii
            lines = alllines[4:]
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
                name = name.split()
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
                data[name] = dict()
                for p in price:
                    # print(count,end="- ")
                    datetime = dates[count]
                    # print(datetime, end= "- ")
                    # print(p)
                    data[name][datetime] = p
                    count += 1

        return data