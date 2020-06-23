from datetime import datetime


class SeniorDiscount:
    """
    This signifies when the senior discount day occurs at the store
    """

    def __init__(self, start_time, end_time, min_time_spent, max_time_spent, percent, day_name='Tuesday'):
        self.start_time = start_time
        self.end_time = end_time
        self.min_time_spent = min_time_spent
        self.max_time_spent = max_time_spent
        self.percent = percent
        self.day_name = day_name

    @property
    def start_time(self):
        """Return the start time."""
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Set the start time."""
        try:
            start_time = datetime.strptime(start_time, '%H:%M').time()
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the start time because the provided start time ({}) is"
                                 " not a string in valid format (21:00).".format(start_time))

        try:
            if start_time < self._end_time:
                self._start_time = start_time
            else:
                raise ValueError("Invalid. Could not set the start time because the provided start time ({}) is"
                                 " greater than the end time({}).".format(start_time, self._end_time))
        except AttributeError:
            self._start_time = start_time

    @property
    def end_time(self):
        """Return the end time."""
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Set the end time."""
        try:
            datetime.strptime(end_time, '%H:%M').time()
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the end time because the provided end time ({}) is"
                                 " not a string in valid format (21:00).".format(end_time))
        a_end_time = datetime.strptime(end_time, '%H:%M').time()
        try:
            if a_end_time > self._open_time:
                self._end_time = a_end_time
            else:
                raise ValueError("Invalid. Could not set the end time because the provided end time ({}) is"
                                 " less than the open time({}).".format(end_time, self._open_time))
        except AttributeError:
            self._end_time = a_end_time
