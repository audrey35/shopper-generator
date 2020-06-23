"""
The Day represent a specific day for the grocery store. It contains necessary information
to generate a list of shoppers that visited the store at the specific date.
"""

import datetime
import calendar

from numpy import random, array
from shoppermodel.shopper import Shopper
from shoppermodel import Util


class Day:
    """
    The Day represent a specific day for the grocery store. It contains necessary information
    to generate a list of shoppers that visited the store at the specific date.
    """
    def __init__(self, store_model, num_of_shoppers, date):
        """
        Initializes Day.
        :param store_model: StoreModel object.
        :param num_of_shoppers: number of shoppers to generate(int).
        :param date: date as datetime object.
        """
        self.store_model = store_model
        self.open_time = store_model.open_time
        self.close_time = store_model.close_time
        self.date = date
        self.num_of_shoppers = num_of_shoppers
        self.day_of_week = calendar.day_name[date.dayofweek]
        self.percent_senior = store_model.percent_senior
        self.shoppers = {"Date": [], "DayOfWeek": [], "TimeIn": [], "TimeSpent": [],
                         "IsSenior": [], "IsSunny": []}
        self.sunny_modifiers = self.store_model.sunny_modifiers
        probability = [self.sunny_modifiers.sunny_chance_percent,
                       1 - self.sunny_modifiers.sunny_chance_percent]
        self.is_sunny = random.choice(a=array([True, False]), p=probability)
        if date.dayofweek in [5, 6]:
            self.is_weekend = True
        else:
            self.is_weekend = False

    def create_shoppers(self):
        """
        Creates a list of shoppers that visited the store at the specific date.
        """
        lunch_percent = self.store_model.lunch_rush.percent
        lunch_start = datetime.datetime.combine(self.date, self.store_model.lunch_rush.start_time)
        lunch_end = datetime.datetime.combine(self.date, self.store_model.lunch_rush.end_time)
        lunch_avg_time_spent = self.store_model.lunch_rush.time_spent

        dinner_percent = self.store_model.dinner_rush.percent
        dinner_start = datetime.datetime.combine(self.date, self.store_model.dinner_rush.start_time)
        dinner_end = datetime.datetime.combine(self.date, self.store_model.dinner_rush.end_time)
        dinner_avg_time_spent = self.store_model.dinner_rush.time_spent

        senior_start = datetime.datetime.combine(self.date,
                                                 self.store_model.senior_discount.start_time)
        senior_end = datetime.datetime.combine(self.date, self.store_model.senior_discount.end_time)
        senior_max_time_spent = self.store_model.senior_discount.max_time_spent
        senior_min_time_spent = self.store_model.senior_discount.min_time_spent

        # TODO weekend values
        weekend_increase = 0.4
        weekend_avg_time_spent = 60
        sunny_weekend_avg_time_spent = self.sunny_modifiers.sunny_time_spent

        times = Util.random_datetimes(datetime.datetime.combine(self.date, self.open_time),
                                      datetime.datetime.combine(self.date, self.close_time),
                                      self.num_of_shoppers)

        for time_in in times:
            new_shopper = Shopper(self, time_in, self.is_sunny,
                                          self.store_model.percent_senior)
            # lunch_percent more lunch shoppers than any other time
            if random.rand() < lunch_percent:
                if not lunch_start < new_shopper.time_in < lunch_end:
                    temp = Util.random_datetimes(lunch_start, lunch_end, 1)
                    new_shopper.time_in = temp[0]
                    new_shopper.time_spent = lunch_avg_time_spent
            # dinner_percent more dinner shoppers than any other time
            if random.rand() < dinner_percent:
                if not dinner_start < new_shopper.time_in < dinner_end:
                    temp = Util.random_datetimes(dinner_start, dinner_end, 1)
                    new_shopper.time_in = temp[0]
                    new_shopper.time_spent = dinner_avg_time_spent
            # check weekend
            if self.is_weekend:
                if self.is_sunny and random.rand() < weekend_increase:
                    new_shopper.time_spent = sunny_weekend_avg_time_spent
                else:
                    new_shopper.time_spent = weekend_avg_time_spent
            # senior hours
            if calendar.day_name[self.date.dayofweek] == self.store_model.senior_discount.day_name:
                if not senior_start < new_shopper.time_in < senior_end:
                    temp = Util.random_datetimes(senior_start, senior_end, 1)
                    new_shopper.time_in = temp[0]
                    new_shopper.time_spent = random.randint(senior_min_time_spent,
                                                            senior_max_time_spent)

            for key, value in new_shopper.shopper_parameters_to_dictionary().items():
                self.shoppers[key].append(value)
