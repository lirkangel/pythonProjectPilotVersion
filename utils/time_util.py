import asyncio
import datetime
import time
from calendar import calendar

from logzero import logger as log

from models.const import CONST_TIMEZONE


class TimerMeasure:
    label: str = ""

    def __init__(self, label: str):
        self.label = label
        self.start = time.time()

    def end(self):
        end = time.time()
        dur = end - self.start

        log.debug(f'{self.label}: {dur:.4f}s')

    @staticmethod
    def start(label: str):
        return TimerMeasure(label)


def timing(func):
    async def process(func, *args, **params):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **params)
        else:
            return func(*args, **params)

    async def helper(*args, **params):
        timer = TimerMeasure.start(func.__name__)
        start = time.time()
        result = await process(func, *args, **params)

        # Test normal function route...
        # result = await process(lambda *a, **p: print(*a, **p), *args, **params)

        timer.end()
        return result

    return helper


def truncate_hms(input_date: datetime):
    input_date = input_date.replace(hour=0, minute=0, second=0, microsecond=0)
    return input_date


"""
Expecting start_time and end_time will be epoch time
"""


def minute_ago(input_epoch: int):
    return int((datetime.datetime.now() + datetime.timedelta(minutes=input_epoch)).timestamp())


epoch = datetime.datetime.utcfromtimestamp(0)


def weeks_from_epoch(_time):
    date = datetime.datetime.utcfromtimestamp(_time)
    d = date - epoch
    return int(d.days / 7)


def time_bucket(_time: float, hours: int) -> int:
    _time = _time or time.time()
    bucket_id = int(_time / 3600 / hours)  # 4 hours each
    return bucket_id


def ago(days: int):
    _ago = calendar.timegm((datetime.date.today() + datetime.timedelta(days=days)).timetuple())
    return _ago


def ago_with_format(days: int):
    return (datetime.date.today() + datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')


def end_of_date(_time):
    date = datetime.datetime.fromtimestamp(_time, tz=CONST_TIMEZONE)
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + datetime.timedelta(1)
    return end


def get_start_and_end():
    tz = CONST_TIMEZONE
    today = datetime.datetime.now(tz=tz)
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + datetime.timedelta(1)

    return start, end
