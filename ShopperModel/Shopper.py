import random


class Shopper:

    def __init__(self, day, time_in):
        self.date = day.date
        self.day_of_week = day.day_of_week
        self.time_in = time_in
        self.time_spent = self.__generate_time_spent()
        self.is_senior = False

    def __generate_time_spent(self):
        return round(random.triangular(6, 75, 25))

    def shopper_parameters_to_dictionary(self):
        return {'Date': self.date, "DayOfWeek": self.day_of_week, "TimeIn": self.time_in, "TimeSpent": self.time_spent,
                "IsSenior": self.is_senior}


class LunchShopper(Shopper):

    def __init__(self, date, time_in):
        super().__init__(date, time_in)
        self.time_spent = self.__generate_time_spent()

    def __generate_time_spent(self):
        return 10


class DinnerShopper(Shopper):

    def __init__(self, date, time_in):
        super().__init__(date, time_in)
        self.time_spent = self.__generate_time_spent()

    def __generate_time_spent(self):
        return 20


class SeniorShopper(Shopper):

    def __init__(self, date, time_in):
        super().__init__(date, time_in)
        self.time_spent = self.__generate_time_spent()
        self.is_senior = True

    def __generate_time_spent(self):
        return random.randint(45, 60)


class WeekendShopper(Shopper):

    def __init__(self, date, time_in):
        super().__init__(date, time_in)
        self.time_spent = self.__generate_time_spent()

    def __generate_time_spent(self):
        return round(random.triangular(6, 75, 60))
