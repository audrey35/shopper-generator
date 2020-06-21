from Shoppers import DayOfWeekConfiguration, HolidayConfiguration
from Shoppers import WeekdayConfiguration, WeekendConfiguration
from Shoppers import LunchRushConfiguration, DinnerRushConfiguration, SeniorRushConfiguration
from Shoppers import DayOfWeek, Holiday, Weekday, Weekend, LunchRush, DinnerRush, SeniorRush
from datetime import datetime as dt


def main():
    dates = []
    # Initialize Configurations and Traffic classes
    day_of_week_config = DayOfWeekConfiguration()
    day_of_week = DayOfWeek(day_of_week_config)
    holiday_config = HolidayConfiguration()
    holiday = Holiday(holiday_config)

    # Initialize Configurations and TimeSpent classes
    weekday_config = WeekdayConfiguration()
    weekday = Weekday(weekday_config)
    weekend_config = WeekendConfiguration()
    weekend = Weekend(weekend_config)

    # Initialize Configurations and Rush classes
    lunch_config = LunchRushConfiguration()
    lunch_rush = LunchRush(lunch_config)
    dinner_config = DinnerRushConfiguration()
    dinner_rush = DinnerRush(dinner_config)
    senior_config = SeniorRushConfiguration()
    senior_rush = SeniorRush(senior_config)

    date = dt(2019, 12, 24)
    avg_traffic = day_of_week.get_average_shopper_traffic(date)
    day_of_week_str = day_of_week.get_day_of_week(date)
    avg_traffic, num_day_holiday = holiday.get_average_shopper_traffic(date, avg_traffic)

    day_dict, hour_traffic = weekday.get_day_dictionary(date, avg_traffic, day_of_week_str,
                                                        num_day_holiday)
    if day_dict == {}:
        day_dict, hour_traffic = weekend.get_day_dictionary(date, avg_traffic, day_of_week_str,
                                                            num_day_holiday)
    print(day_of_week_str)
    print(avg_traffic)
    print(hour_traffic)
    print(len(day_dict["Date"]))

    day_dict = lunch_rush.get_day_dictionary(day_dict, hour_traffic)
    print()
    print(len(day_dict["Date"]))

    day_dict = dinner_rush.get_day_dictionary(day_dict, hour_traffic)
    print()
    print(len(day_dict["Date"]))

    temp_dict = senior_rush.get_day_dictionary(day_dict, hour_traffic)
    if temp_dict != {}:
        day_dict = temp_dict
        print()
        print(len(day_dict["Date"]))


    #for date in dates:
    #    traffic = day_of_week.get_average_shopper_traffic(date)

if __name__ == '__main__':
    main()
