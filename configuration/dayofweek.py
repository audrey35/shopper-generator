"""Represents average number of shoppers visiting the store on a given day of week."""


class DayOfWeek:
    """Represents average number of shoppers visiting the store on a given day of week."""

    def __init__(self, day_name, shopper_traffic):
        """
        Initializes DayOfWeek.
        :param day_name: name of the given day of week (Monday-Sunday).
        :param shopper_traffic: average number of shoppers visiting the store on the day of week.
        """
        self.day_name = day_name
        self.shopper_traffic = shopper_traffic
