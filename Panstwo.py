class Kraj:
    def __init__(self, country_name, dane_ceny):
        self.__name = country_name
        self.__ceny = dict()
        self.__add_data(dane_ceny)
        self.__status = False

    def __add_data(self, dictionary):
        for name, item in dictionary.items():
            # przenosi dane z zewnętrzengo słownika do klasy odpowiadającej danemy państwu
            if name == self.__name:
                for date, price in item.items():
                    self.__ceny[date] = price

    def get_dates_and_cost(self):
        return self.__ceny

    def get_name(self):
        return self.__name

    def flip_status(self):
        self.__status = not self.__status

    def get_status(self):
        return self.__status

    def __repr__(self):
        nazwa = self.__class__.__name__
        atrybuty = {k.split("__")[-1]: v for k, v in self.__dict__.items()}
        return f"{nazwa}: {atrybuty} "
