
from Wykres import Rysuj
from CzytnikPliku import Czytnik

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
    NowyCzytnik = Czytnik()

    sciezka = input("sciezka")
    dane = NowyCzytnik.read_file(sciezka)
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


    lista = list()
    lista.append(Belgium)
    lista.append(Bosnia)
    lista.append(Kosovo)
    lista.append(Ireland)
    lista.append(Spain)

    Rysownik = Rysuj()
    start_date = input("data początkową")
    end_date = input("data konca ")
    Rysownik.wykres(lista,start_date,end_date)


