import re

pg_time_intervals = ['microseconds', 'milliseconds', 'second', 'minute', 'hour', 'day', 'week',
                     'month', 'quarter', 'year', 'decade', 'century', 'millennium']


def validate_timeinterval_units(time_interval: str) -> bool:
    if re.fullmatch(r"\d+\s[a-zA-Z]+$", time_interval):
        pattern = r"[a-zA-Z]+$"
        interval = re.search(pattern, time_interval).group(0)
        return True if interval in pg_time_intervals else False
    else:
        return False

