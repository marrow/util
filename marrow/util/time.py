# encoding: utf-8

from datetime import timedelta, tzinfo


__all__ = [
        'UTC', 'delta_to_seconds',
        'day', 'week', 'hour', 'minute', 'second', 'month', 'year'
        'minute_range', 'hour_range', 'dom_range', 'month_range', 'dow_range',
        'map_month', 'map_dow'
    ]



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

minute_range = (0, 59)
hour_range = (0, 23)
dom_range = (1, 31)
month_range = (1, 12)
dow_range = (0, 7)

_month_map = dict(jan=1, feb=2, mar=3, apr=4, may=5, jun=6, jul=7, aug=8, sep=9, oct=10, nov=11, dec=12)
_dow_map = dict(sun=0, mon=1, tue=2, wed=3, thu=4, fri=5, sat=6)

def _map(mapper):
    def inner(value):
        value = value.lower()
        
        for i in mapper:
            if value.startswith(i):
                return mapper[i]

        return None

    return inner

map_month = _map(_month_map)
map_dow = _map(_dow_map)
