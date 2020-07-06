""""
Contains all modifier variables for a sunny day
"""
import random


class DayModifiers:
    """
    Contains all modifier variables for weekends and sunny days
    """

    def __init__(self, min_time_spent=6, avg_time_spent=25, max_time_spent=75,
                 weekend_time_spent=60, sunny_traffic_percent=0.4,
                 sunny_chance_percent=0.3, sunny_time_spent=15):
        self.min_time_spent = min_time_spent
        self.avg_time_spent = avg_time_spent
        self.max_time_spent = max_time_spent
        self.weekend_time_spent = weekend_time_spent
        self.sunny_traffic_percent = sunny_traffic_percent
        self.sunny_chance_percent = sunny_chance_percent
        self.sunny_time_spent = sunny_time_spent

    def time_spent(self, is_weekend=False):
        if not is_weekend:
            return random.triangular(self.min_time_spent, self.avg_time_spent, self.max_time_spent)
        else:
            return random.triangular(self.min_time_spent, self.weekend_time_spent, self.max_time_spent)
