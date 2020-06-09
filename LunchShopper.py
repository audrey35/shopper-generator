import Shopper


class LunchShopper(Shopper):

    def __init__(self, date, time_in):
        super().__init__(date, time_in)
        self.time_spent = self.__generate_time_spent()

    def __generate_time_spent(self):
        return 10
