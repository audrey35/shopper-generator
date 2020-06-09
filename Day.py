import Shopper
import datetime
import Util
import pandas as pd
import numpy as np
import random


class Day:

    def __init__(self, open_time, close_time, date, num_of_shoppers,
                 lunch_rush=None, dinner_rush=None, senior_rush=None):
        self.date = date
        self.open_time = open_time
        self.close_time = close_time
        self.num_of_shoppers = num_of_shoppers # 800
        self.lunch_rush = lunch_rush
        self.dinner_rush = dinner_rush
        self.senior_rush = senior_rush

    def create_shoppers(self):

        lunch_shoppers = round(self.num_of_shoppers * 0.1) # 80
        dinner_shoppers = round(self.num_of_shoppers * 0.15) # 120
        overall_shoppers = self.num_of_shoppers - lunch_shoppers - dinner_shoppers # 600

        lunch_start = datetime.time(12, 0)
        lunch_end = datetime.time(13, 0)

        dinner_start = datetime.time(17, 0)
        dinner_end = datetime.time(18, 30)

        times = Util.random_datetimes(pd.Timestamp.combine(self.date, self.open_time),
                                      pd.Timestamp.combine(self.date, self.close_time),
                                      overall_shoppers)

        lunch_times = Util.random_datetimes(pd.Timestamp.combine(self.date, lunch_start),
                                            pd.Timestamp.combine(self.date, lunch_end),
                                            lunch_shoppers)

        dinner_times = Util.random_datetimes(pd.Timestamp.combine(self.date, dinner_start),
                                             pd.Timestamp.combine(self.date, dinner_end),
                                             dinner_shoppers)

        shoppers = []

        for time_in in times:
            shoppers.append(Shopper.Shopper(self.date, time_in, round(random.triangular(6, 75, 25))))

        for time_in in lunch_times:
            shoppers.append(Shopper.Shopper(self.date, time_in, 10))

        for time_in in dinner_times:
            shoppers.append(Shopper.Shopper(self.date, time_in, 20))

        return shoppers
