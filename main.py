
from Wykres import Rysuj

p

def read_file(filepath):
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

            # prices = " ".join(price)
            # prices.strip('" ')
            # print(name)
            # print(prices)

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


class Kraj:
    def __init__(self, country_name, dane_ceny):
        self.__name = country_name
        self.__ceny = dict()
        self.__add_data(dane_ceny)

    def __add_data(self, dictionary):
        for name, item in dictionary.items():
            # przenosi dane z zewnętrzengo słownika do klasy odpowiadającej danemy państwu
            if name == self.__name:
                # print(name)
                # print(item)
                for date, price in item.items():
                    self.__ceny[date] = price

    def get_dates_and_cost(self):
        return self.__ceny

    def get_name(self):
        return self.__name

    def __repr__(self):
        nazwa = self.__class__.__name__
        atrybuty = {k.split("__")[-1]: v for k, v in self.__dict__.items()}
        return f"{nazwa}: {atrybuty} "


if __name__ == '__main__':
    dane = read_file(
        'Electricity prices for household consumers - bi-annual data (from 2007 onwards) [NRG_PC_204].csv')
    print(dane)

    Belgium = Kraj("Belgium", dane)
    print(Belgium)

    proba = Belgium.get_dates_and_cost()
    print("test")
    print(proba)

    Czechia = Kraj("Czechia", dane)
    print(Czechia)

    Germany = Kraj("Germany", dane)
    print(Germany)

    Ireland = Kraj("Ireland", dane)
    print(Ireland)

    Spain = Kraj("Spain", dane)
    print(Spain)

    Kosovo = Kraj("Kosovo", dane)
    print(Kosovo)

    Bosnia = Kraj("Bosnia", dane)
    print(Bosnia)

    Rysownik = Rysuj()
    lista = list()
    lista.append(Belgium)
    lista.append(Bosnia)
    lista.append(Kosovo)
    lista.append(Ireland)
    lista.append(Spain)
    Rysownik.wykres(lista,"2009-S2",'2013-S2')


