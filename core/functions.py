import time


def get_unix_time(time_string: str) -> int:
    '''Конвертирует время в формат unix'''
    return time.mktime(time.strptime(time_string, '%H:%M %d.%m.%Y'))


def convert_time(seconds: int, string_format: str):
  return time.strftime(string_format, time.localtime(seconds))