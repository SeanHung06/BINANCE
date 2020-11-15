
import time
import datetime
from datetime import date

def transform_time(df):
    return df.apply(lambda d: datetime.datetime.fromtimestamp(int(d)/1000).strftime('%Y-%m-%d %H:%M:%S'))