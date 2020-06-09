import SeniorShopper
import DinnerShopper
import WeekendShopper
import Shopper
import LunchShopper
import datetime
import Util
import pandas as pd
import numpy as np


class Day:

    def __init__(self, open_time, close_time, date, num_of_shoppers, percent_senior):
        self.open_time = open_time
        self.close_time = close_time
        self.date = date
        self.num_of_shoppers = num_of_shoppers # 800
        self.percent_senior = percent_senior
        if date.dayofweek in [5, 6]:
            self.is_weekend = True
        else:
            self.is_weekend = False

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
            if np.random.choice(a=np.array([True, False]), p=[self.percent_senior, 1 - self.percent_senior]):
                shoppers.append(SeniorShopper.SeniorShopper(self.date, time_in))
            else:
                if self.is_weekend:
                    shoppers.append(WeekendShopper.WeekendShopper(self.date, time_in))
                else:
                    shoppers.append(Shopper.Shopper(self.date, time_in))

        for time_in in lunch_times:
            shoppers.append(LunchShopper.LunchShopper(self.date, time_in))

        for time_in in dinner_times:
            shoppers.append(DinnerShopper.DinnerShopper(self.date, time_in))

        return shoppers
