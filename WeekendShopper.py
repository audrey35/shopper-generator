import Shopper
import random


class WeekendShopper(Shopper):

    def __init__(self, date, time_in):
        self.date = date
        self.time_in = time_in
        self.time_spent = self.__generate_time_spent()

    def __generate_time_spent(self):
        return round(random.triangular(6, 75, 60))
