from datetime import datetime


class Configuration:
    """
    The Configuration contains all of the parameters that can be set by the user to change
    the generated table.
    """
    def __init__(self, start_date: str, end_date: str, open_time: str, close_time: str, mon_avg_traffic: int,
                 tues_avg_traffic: int, wed_avg_traffic: int, thurs_avg_traffic: int, fri_avg_traffic: int,
                 sat_avg_traffic: int, sun_avg_traffic: int, lunchtime_percent: float, dinnertime_percent: int,
                 senior_percent: float, senior_discount_percent: float,
                 min_time_spent: int, avg_time_spent: int, max_time_spent: int,
                 lunch_avg_time_spent: int, dinner_avg_time_spent: int,
                 weekend_avg_time_spent: int, sunny_weekend_avg_time_spent: int,
                 senior_min_time_spent: int, senior_max_time_spent: int):
        self.start_date = start_date
        self.end_date = end_date
        self.open_time = open_time
        self.close_time = close_time
        self.mon_avg_traffic = mon_avg_traffic
        self.tues_avg_traffic = tues_avg_traffic
        self.wed_avg_traffic = wed_avg_traffic
        self.thurs_avg_traffic = thurs_avg_traffic
        self.fri_avg_traffic = fri_avg_traffic
        self.sat_avg_traffic = sat_avg_traffic
        self.sun_avg_traffic = sun_avg_traffic
        self.lunchtime_percent = lunchtime_percent
        self.dinnertime_percent = dinnertime_percent
        self.senior_percent = senior_percent
        self.senior_discount_percent = senior_discount_percent
        self.min_time_spent = min_time_spent
        self.avg_time_spent = avg_time_spent
        self.max_time_spent = max_time_spent
        self.lunch_avg_time_spent = lunch_avg_time_spent
        self.dinner_avg_time_spent = dinner_avg_time_spent
        self.weekend_avg_time_spent = weekend_avg_time_spent
        self.sunny_weekend_avg_time_spent = sunny_weekend_avg_time_spent
        self.senior_min_time_spent = senior_min_time_spent
        self.senior_max_time_spent = senior_max_time_spent

    @property
    def start_date(self):
        """Return the start date."""
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Set the start date."""
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise AttributeError("Invalid. Could not set the start date because the provided start date({}) is not "
                                 "a string in valid format (2018-01-01).".format(start_date))
        a_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        try:
            if a_start_date < self.end_date:
                self._start_date = a_start_date
            else:
                raise ValueError("Invalid. Could not set the start date because the provided start date ({}) "
                                     "is greater than the end date({}).".format(start_date, self.end_date))
        except AttributeError:
            self._start_date = a_start_date

    @property
    def end_date(self):
        """Return the end date."""
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Set the end date."""
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise AttributeError("Invalid. Could not set the end date because the provided end date({}) is not "
                                 "a string in valid format (2018-01-01).".format(end_date))
        a_end_date = datetime.strptime(end_date, "%Y-%m-%d")
        try:
            if a_end_date > self._start_date:
                self._end_date = a_end_date
            else:
                raise ValueError("Invalid. Could not set the end date because the provided end date ({}) "
                                     "should be greater than the start date({}).".format(end_date, self._start_date))
        except AttributeError:
            self._end_date = a_end_date

    @property
    def open_time(self):
        """Return the open time."""
        return self._open_time

    @open_time.setter
    def open_time(self, open_time):
        """Set the open time."""
        try:
            open_time = datetime.strptime(open_time, '%H:%M').time()
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the open time because the provided open time ({}) is"
                                 " not a string in valid format (21:00).".format(open_time))

        try:
            if open_time < self._close_time:
                self._open_time = open_time
            else:
                raise ValueError("Invalid. Could not set the open time because the provided open time ({}) is"
                                     " greater than the close time({}).".format(open_time, self._close_time))
        except AttributeError:
            self._open_time = open_time

    @property
    def close_time(self):
        """Return the close time."""
        return self._close_time

    @close_time.setter
    def close_time(self, close_time):
        """Set the close time."""
        try:
            datetime.strptime(close_time, '%H:%M').time()
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the close time because the provided close time ({}) is"
                                 " not a string in valid format (21:00).".format(close_time))
        a_close_time = datetime.strptime(close_time, '%H:%M').time()
        try:
            if a_close_time > self._open_time:
                self._close_time = a_close_time
            else:
                raise ValueError("Invalid. Could not set the close time because the provided close time ({}) is"
                                 " less than the open time({}).".format(close_time, self._open_time))
        except AttributeError:
            self._close_time = a_close_time

    @property
    def mon_avg_traffic(self):
        """Return the average traffic for Monday."""
        return self._mon_avg_traffic

    @mon_avg_traffic.setter
    def mon_avg_traffic(self, mon_avg_traffic):
        """Set the average traffic for Monday."""
        try:
            mon_avg_traffic = int(mon_avg_traffic)
        except ValueError:
            raise AttributeError("Invalid. Could not set the average traffic for Monday because the provided value "
                                 "({}) is not an integer.".format(mon_avg_traffic))
        if mon_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Monday because the value ({})"
                                 " is less than 0.".format(mon_avg_traffic))
        self._mon_avg_traffic = mon_avg_traffic

    @property
    def tues_avg_traffic(self):
        """Return the average traffic for Tuesday."""
        return self._tues_avg_traffic

    @tues_avg_traffic.setter
    def tues_avg_traffic(self, tues_avg_traffic):
        """Set the average traffic for Tuesday."""
        try:
            tues_avg_traffic = int(tues_avg_traffic)
        except ValueError:
            raise AttributeError("Invalid. Could not set the average traffic for Tuesday because the provided value "
                                 "({}) is not an integer.".format(tues_avg_traffic))
        if tues_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Tuesday because the value ({})"
                                 " is less than 0.".format(tues_avg_traffic))
        self._tues_avg_traffic = tues_avg_traffic

    @property
    def wed_avg_traffic(self):
        """Return the average traffic for Wednesday."""
        return self._wed_avg_traffic

    @wed_avg_traffic.setter
    def wed_avg_traffic(self, wed_avg_traffic):
        """Set the average traffic for Wednesday."""
        try:
            wed_avg_traffic = int(wed_avg_traffic)
        except ValueError:
            raise AttributeError("Invalid. Could not set the average traffic for Wednesday because the provided value "
                                 "({}) is not an integer.".format(wed_avg_traffic))
        if wed_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Wednesday because the value ({})"
                                 " is less than 0.".format(wed_avg_traffic))
        self._wed_avg_traffic = wed_avg_traffic

    @property
    def thurs_avg_traffic(self):
        """Return the average traffic for Thursday."""
        return self._thurs_avg_traffic

    @thurs_avg_traffic.setter
    def thurs_avg_traffic(self, thurs_avg_traffic):
        """Set the average traffic for Thursday."""
        try:
            thurs_avg_traffic = int(thurs_avg_traffic)
        except ValueError:
            raise AttributeError("Invalid. Could not set the average traffic for Thursday because the provided value "
                                 "({}) is not an integer.".format(thurs_avg_traffic))
        if thurs_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Thursday because the value ({})"
                                 " is less than 0.".format(thurs_avg_traffic))
        self._thurs_avg_traffic = thurs_avg_traffic

    @property
    def fri_avg_traffic(self):
        """Return the average traffic for Friday."""
        return self._fri_avg_traffic

    @fri_avg_traffic.setter
    def fri_avg_traffic(self, fri_avg_traffic):
        """Set the average traffic for Friday."""
        try:
            fri_avg_traffic = int(fri_avg_traffic)
        except ValueError:
            raise AttributeError("Invalid. Could not set the average traffic for Friday because the provided value "
                                 "({}) is not an integer.".format(fri_avg_traffic))
        if fri_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Friday because the value ({})"
                                 " is less than 0.".format(fri_avg_traffic))
        self._fri_avg_traffic = fri_avg_traffic

    @property
    def sat_avg_traffic(self):
        """Return the average traffic for Saturday."""
        return self._sat_avg_traffic

    @sat_avg_traffic.setter
    def sat_avg_traffic(self, sat_avg_traffic):
        """Set the average traffic for Saturday."""
        try:
            sat_avg_traffic = int(sat_avg_traffic)
        except ValueError:
            raise AttributeError("Invalid. Could not set the average traffic for Saturday because the provided value "
                                 "({}) is not an integer.".format(sat_avg_traffic))
        if sat_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Saturday because the value ({})"
                                 " is less than 0.".format(sat_avg_traffic))
        self._sat_avg_traffic = sat_avg_traffic

    @property
    def sun_avg_traffic(self):
        """Return the average traffic for Sunday."""
        return self._sun_avg_traffic

    @sun_avg_traffic.setter
    def sun_avg_traffic(self, sun_avg_traffic):
        """Set the average traffic for Sunday."""
        try:
            sun_avg_traffic = int(sun_avg_traffic)
        except ValueError:
            raise AttributeError("Invalid. Could not set the average traffic for Sunday because the provided value "
                                 "({}) is not an integer.".format(sun_avg_traffic))
        if sun_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Sunday because the value ({})"
                                 " is less than 0.".format(sun_avg_traffic))
        self._sun_avg_traffic = sun_avg_traffic

    @property
    def lunchtime_percent(self):
        """Return the percentage of shoppers coming in at lunchtime."""
        return self._lunchtime_percent

    @lunchtime_percent.setter
    def lunchtime_percent(self, lunchtime_percent):
        """Set the percentage of shoppers coming in at lunchtime."""
        try:
            lunchtime_percent = float(lunchtime_percent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the percentage of shoppers coming in at lunchtime"
                                 " because the provided value ({}) is not a float.".format(lunchtime_percent))
        if lunchtime_percent < 0:
            raise AttributeError("Invalid. Could not set the percentage of shoppers coming in at lunchtime"
                                 " because the value ({}) is less than 0.".format(lunchtime_percent))
        self._lunchtime_percent = lunchtime_percent

    @property
    def dinnertime_percent(self):
        """Return the percentage of shoppers coming in at dinnertime."""
        return self._dinnertime_percent

    @dinnertime_percent.setter
    def dinnertime_percent(self, dinnertime_percent):
        """Set the percentage of shoppers coming in at dinnertime."""
        try:
            dinnertime_percent = float(dinnertime_percent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the percentage of shoppers coming in at dinnertime"
                                 " because the provided value ({}) is not a float.".format(dinnertime_percent))
        if dinnertime_percent < 0:
            raise AttributeError("Invalid. Could not set the percentage of shoppers coming in at dinnertime"
                                 " because the value ({}) is less than 0.".format(dinnertime_percent))
        self._dinnertime_percent = dinnertime_percent

    @property
    def senior_percent(self):
        """Return the percentage of seniors coming in at any given hour."""
        return self._senior_percent

    @senior_percent.setter
    def senior_percent(self, senior_percent):
        """Set the percentage of seniors coming in at any given hour."""
        try:
            senior_percent = float(senior_percent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the percentage of seniors coming in at any given hour"
                                 " because the provided value ({}) is not a float.".format(senior_percent))
        if senior_percent < 0:
            raise AttributeError("Invalid. Could not set the percentage of seniors coming in at any given hour"
                                 " because the value ({}) is less than 0.".format(senior_percent))
        self._senior_percent = senior_percent

    @property
    def senior_discount_percent(self):
        """Return the percentage of seniors coming in on Tuesday 10-12pm."""
        return self._senior_discount_percent

    @senior_discount_percent.setter
    def senior_discount_percent(self, senior_discount_percent):
        """Set the percentage of seniors coming in on Tuesday 10-12pm."""
        try:
            senior_discount_percent = float(senior_discount_percent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the percentage of seniors coming in  on Tuesday 10-12pm"
                                 " because the provided value ({}) is not a float.".format(senior_discount_percent))
        if senior_discount_percent < 0:
            raise AttributeError("Invalid. Could not set the percentage of seniors coming in on Tuesday 10-12pm"
                                 " because the value ({}) is less than 0.".format(senior_discount_percent))
        self._senior_discount_percent = senior_discount_percent

    @property
    def min_time_spent(self):
        """Return the minimum time a shopper spent in the store (in minutes)."""
        return self._min_time_spent

    @min_time_spent.setter
    def min_time_spent(self, min_time_spent):
        """Set the minimum time a shopper spent in the store (in minutes)."""
        try:
            min_time_spent = int(min_time_spent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the minimum time spent because the provided value "
                                 "({}) is not an integer.".format(min_time_spent))
        if min_time_spent < 0:
            raise AttributeError("Invalid. Could not set the minimum time spent because the value ({})"
                                 " is less than 0.".format(min_time_spent))
        self._min_time_spent = min_time_spent

    @property
    def avg_time_spent(self):
        """Return the average time a shopper spent in the store (in minutes)."""
        return self._avg_time_spent

    @avg_time_spent.setter
    def avg_time_spent(self, avg_time_spent):
        """Set the average time a shopper spent in the store (in minutes)."""
        try:
            avg_time_spent = int(avg_time_spent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the average time spent because the provided value "
                                 "({}) is not an integer.".format(avg_time_spent))
        if avg_time_spent < 0:
            raise AttributeError("Invalid. Could not set the average time spent because the value ({})"
                                 " is less than 0.".format(avg_time_spent))
        self._avg_time_spent = avg_time_spent

    @property
    def max_time_spent(self):
        """Return the maximum time a shopper spent in the store (in minutes)."""
        return self._max_time_spent

    @max_time_spent.setter
    def max_time_spent(self, max_time_spent):
        """Set the maximum time a shopper spent in the store (in minutes)."""
        try:
            max_time_spent = int(max_time_spent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the maximum time spent because the provided value "
                                 "({}) is not an integer.".format(max_time_spent))
        if max_time_spent < 0:
            raise AttributeError("Invalid. Could not set the maximum time spent because the value ({})"
                                 " is less than 0.".format(max_time_spent))
        self._max_time_spent = max_time_spent

    @property
    def lunch_avg_time_spent(self):
        """Return the average time a shopper spends in the store at lunchtime."""
        return self._lunch_avg_time_spent

    @lunch_avg_time_spent.setter
    def lunch_avg_time_spent(self, lunch_avg_time_spent):
        """Set the average time a shopper spends in the store at lunchtime."""
        try:
            lunch_avg_time_spent = float(lunch_avg_time_spent)
        except ValueError:
            raise AttributeError(
                "Invalid. Could not set the the average time a shopper spends in the store at lunchtime"
                " because the provided value ({}) is not a float.".format(lunch_avg_time_spent))
        if lunch_avg_time_spent < 0:
            raise AttributeError("Invalid. Could not set the average time a shopper spends in the store at lunchtime"
                                 " because the value ({}) is less than 0.".format(lunch_avg_time_spent))
        self._lunch_avg_time_spent = lunch_avg_time_spent

    @property
    def dinner_avg_time_spent(self):
        """Return the average time a shopper spends in the store at dinnertime."""
        return self._dinner_avg_time_spent

    @dinner_avg_time_spent.setter
    def dinner_avg_time_spent(self, dinner_avg_time_spent):
        """Set the average time a shopper spends in the store at dinnertime."""
        try:
            dinner_avg_time_spent = float(dinner_avg_time_spent)
        except ValueError:
            raise AttributeError(
                "Invalid. Could not set the the average time a shopper spends in the store at dinnertime"
                " because the provided value ({}) is not a float.".format(dinner_avg_time_spent))
        if dinner_avg_time_spent < 0:
            raise AttributeError("Invalid. Could not set the average time a shopper spends in the store at dinnertime"
                                 " because the value ({}) is less than 0.".format(dinner_avg_time_spent))
        self._dinner_avg_time_spent = dinner_avg_time_spent

    @property
    def senior_min_time_spent(self):
        """Return the minimum time a senior shopper spends in the store during senior discount hours."""
        return self._senior_min_time_spent

    @senior_min_time_spent.setter
    def senior_min_time_spent(self, senior_min_time_spent):
        """Set the minimum time a senior shopper spends in the store during senior discount hours."""
        try:
            senior_min_time_spent = float(senior_min_time_spent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the the minimum time a senior shopper spends in the store "
                                 "during senior discount hours because the provided value ({}) is "
                                 "not a float.".format(senior_min_time_spent))
        if senior_min_time_spent < 0:
            raise AttributeError("Invalid. Could not set the minimum time a senior shopper spends in the store during "
                                 "senior discount hours because the value ({}) is "
                                 "less than 0.".format(senior_min_time_spent))
        self._senior_min_time_spent = senior_min_time_spent

    @property
    def senior_max_time_spent(self):
        """Return the maximum time a senior shopper spends in the store during senior discount hours."""
        return self._senior_max_time_spent

    @senior_max_time_spent.setter
    def senior_max_time_spent(self, senior_max_time_spent):
        """Set the maximum time a senior shopper spends in the store during senior discount hours."""
        try:
            senior_max_time_spent = float(senior_max_time_spent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the the maximum time a senior shopper spends in the store "
                                 "during senior discount hours because the provided value ({}) is "
                                 "not a float.".format(senior_max_time_spent))
        if senior_max_time_spent < 0:
            raise AttributeError("Invalid. Could not set the maximum time a senior shopper spends in the store during "
                                 "senior discount hours because the value ({}) is "
                                 "less than 0.".format(senior_max_time_spent))
        self._senior_max_time_spent = senior_max_time_spent
