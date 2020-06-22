import random
import numpy as np

class Shopper:
    """
    A Shopper that is visiting the store. The constructor takes in the Day the shopper is visiting
    the store at. Uses default values for all fields.
    """
    # TODO regular time values
    normalmintime = 6
    normalmaxtime = 75
    normalavgtime = 25
    # For Carlo:
    # lunch_start and end and dinner_start and end in Day class
    # And lunch_avg_time_spent, dinner_avg_time_spent, weekend_increase, default_senior, default_sunny

    def __init__(self, day, time_in, is_sunny, percent_senior):
        self.date = day.date
        self.day_of_week = day.day_of_week
        self.time_in = time_in
        self.is_sunny = is_sunny
        self.time_spent = self.__generate_time_spent()
        self.percent_senior = percent_senior
        self.is_senior = np.random.choice(a=np.array([True, False]), p=[self.percent_senior, 1 - self.percent_senior])

    def __generate_time_spent(self):
        return round(random.triangular(self.normalmintime, self.normalmaxtime, self.normalavgtime))

    def shopper_parameters_to_dictionary(self):
        return {'Date': self.date, "DayOfWeek": self.day_of_week, "TimeIn": self.time_in, "TimeSpent": self.time_spent,
                "IsSenior": self.is_senior, "IsSunny": self.is_sunny}