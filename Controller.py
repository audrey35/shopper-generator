import Configuration


class Controller:
    """Class Controller for handling user interaction
    and starting the program."""
    def __init__(self, start_date='01/01/2018', end_date='12/31/2019', start_time='06:00', end_time='21:00',
                 mon_avg_traff=800, tues_avg_traff=1000, wed_avg_traff=1200, thurs_avg_traff=900, fri_avg_traff=2500,
                 sat_avg_traff=4000, sun_avg_traff=5000, min_time_spent=6, avg_time_spent=25, max_time_spent=75,
                 daily_avg_senior_percentage=20):
        # TODO: add variables for modifying the table for special cases
        """Initialize each attribute."""
        self.configuration = Configuration(start_date, end_date, start_time, end_time,
                 mon_avg_traff, tues_avg_traff, wed_avg_traff, thurs_avg_traff, fri_avg_traff,
                 sat_avg_traff, sun_avg_traff, min_time_spent, avg_time_spent, max_time_spent,
                 daily_avg_senior_percentage)
        self.model = Model(self.configuration)

    def create_table(self):
        self.model.create_table()