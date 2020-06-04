import shoppers
import pandas as pd
import calendar
import holidays

from datetime import date

if __name__ == '__main__':

    # Possible input: list of shopper counts
    shopper_count_by_day = [800, 1000, 1200, 900, 2500, 4000, 5000]

    # Possible input: start and end date range
    start = '2019-01-01'
    end = '2020-12-31'

    date_list = pd.date_range(start, end)
    print(date_list)

    holidays = holidays.US()

    # create dictionary to fill with values
    shopper_dict = {"DayOfWeek": [], "Date": []}

    # loop through each date
    for date in date_list:
        day_int = date.dayofweek
        day = calendar.day_name[day_int]

        num_of_shoppers = shopper_count_by_day[day_int]
        if date in holidays:
            num_of_shoppers = 0.2 * num_of_shoppers

        # populate dictionary with values
        for n in range(int(num_of_shoppers)):
            shopper_dict["DayOfWeek"].append(day)
            shopper_dict["Date"].append(date.date())

    # convert to dataframe
    df = pd.DataFrame(shopper_dict)
    print(df)

    # # loop through each day
    # while start_date <= end_date:
    #     day_of_week = start_date.weekday()
