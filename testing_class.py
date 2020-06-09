from datetime import datetime, time, date
import pandas as pd
import Day


if __name__ == '__main__':

    open_time = time(6, 0)
    close_time = time(21, 0)

    date = date(2020, 5, 4)

    day = Day.Day(open_time, close_time, date, 1584620)

    shopper_list = day.create_shoppers()
    df = pd.DataFrame(shopper_list)
    print(df)



