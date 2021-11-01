from dateutil.relativedelta import relativedelta
import datetime 

def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def get_ym_now():
    dt = datetime.datetime.now()
    delta = relativedelta(months=12) # 0
    dt = dt - delta
    return dt.strftime("%Y%m")


def get_yms(end_ym="202003"):
    dt = datetime.datetime.now()
    # dt = datetime.datetime(1900, 2, 1) # for debugging
    while True:
        ym = dt.strftime("%Y%m") # 20200401 -> 202004
        yield ym
        if ym == end_ym:
            break
        delta = relativedelta(months=1)
        dt = dt - delta 


def to_datetime(row):
    return datetime.datetime(row['년'], row['월'], row['일']).strftime('%Y-%m-%d %H:%M:%S')


