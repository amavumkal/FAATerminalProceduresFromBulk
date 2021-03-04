import datetime

def get_current_cycl():
    PRESENT = datetime.datetime.now()  # present time
    TIME_DELTA = datetime.timedelta(days=28)  # used to increase date by 28 days. FAA chart cycle
    CYCLE_BASE = datetime.datetime(2021, 1, 28)  # reference point for faa cycles
    date_increment = CYCLE_BASE
    while ((date_increment + TIME_DELTA) <= PRESENT):  # loop while cycle date is less than current date.
        date_increment += TIME_DELTA

    # date_increment = date_increment + TIME_DELTA  # adds TIME_DELTA one more time since faa cycle attribute is based on end of cycle
    cycle_month = str(date_increment.month)
    cycle_day = str(date_increment.day)
    cycle_year = str(date_increment.year)[-2:]
    if (len(cycle_month) == 1):  # if single digit month adds 0 to resulting string
        cycle_month = "0" + cycle_month
    if (len(cycle_day) == 1):  # if single digit month adds 0 to resulting string
        cycle_day = "0" + cycle_day
    return (cycle_year + cycle_month + cycle_day)


def get_four_digit_cycle():
    PRESENT = datetime.datetime.now()  # present time
    TIME_DELTA = datetime.timedelta(days=28)  # used to increase date by 28 days. FAA chart cycle
    CYCLE_BASE = datetime.datetime(2021, 1, 18)  # reference point for faa cycles
    date_increment = CYCLE_BASE
    while ((date_increment + TIME_DELTA) <= PRESENT):  # loop while cycle date is less than current date.
        date_increment += TIME_DELTA
    date_increment -= TIME_DELTA
    cycle_month = str(date_increment.month)
    cycle_year = str(date_increment.year)[-2:]
    if (len(cycle_month) == 1):  # if single digit month adds 0 to resulting string
        cycle_month = "0" + cycle_month
    return (cycle_year + cycle_month)