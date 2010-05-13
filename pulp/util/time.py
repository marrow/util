# encoding: utf-8

from datetime import timedelta, tzinfo


__all__ = ['UTC', 'delta_to_seconds', 'day', 'week', 'hour', 'minute', 'second', 'month', 'year']



class _UTC(tzinfo):
    __repr__ = lambda: 'UTC'
    dst = lambda dt: timedelta(0)
    utcoffset = lambda dt: timedelta(0)
    tzname = lambda dt: 'UTC'

UTC = _UTC()


def delta_to_seconds(self):
    "Convert a timedelta instance to seconds."
    return self.seconds + (self.days * 24 * 60 * 60)


day = timedelta(days=1)
week = timedelta(weeks=1)
hour = timedelta(hours=1)
minute = timedelta(minutes=1)
second = timedelta(seconds=1)
month = timedelta(days=30.4167) # average in non-leap year
year = timedelta(days=365)
