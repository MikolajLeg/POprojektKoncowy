import numpy as np
from matplotlib import pyplot as plt

class Rysuj:

    def __init__(self):
        pass

    def wykres(self,Kraje,start_date,end_date):
        alldates = dict()
        allcosts = dict()
        lgd =list()
        min = 1
        max = 0
        for kraj in Kraje:
            dates = list()
            costs = list()
            check = False
            for date,cost in kraj.get_dates_and_cost().items():
                if date == start_date:
                    check = not check
                elif date == end_date:
                    check = not check
                if cost == 'no data':
                    continue
                if cost < min:
                    min = cost
                if cost > max :
                    max = cost

                if check == True:
                    dates.append(date)
                    costs.append(cost)
p
            lgd.append(kraj.get_name())

            alldates[kraj] =dates
            allcosts[kraj] = costs

        for kraj in Kraje:
            plt.plot(alldates[kraj],allcosts[kraj])
        min = min.__round__(2)
        max = max.__round__(2)
        plt.yticks(np.arange(min,max,0.1))
        plt.xlabel("data")
        plt.ylabel("koszt")
        plt.title("Koszta energii w danym kraju")
        plt.legend(lgd)
        plt.show()
