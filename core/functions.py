import datetime
from pytz import timezone


def get_unix_time(time_string: str) -> int:
    return int(datetime.datetime.strptime(time_string, "%d.%m.%Y %H:%M").timestamp())


def convert_time(seconds: int, string_format: str) -> str:
    return datetime.datetime.fromtimestamp(seconds, timezone("Europe/Moscow")).strftime(string_format)  