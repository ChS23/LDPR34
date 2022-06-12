import datetime


def getTimeUnix(time:str) -> int:
    '''Конвертирует время в формат unix'''
    return int(datetime.datetime.strptime(time, "%d.%m.%Y %H:%M").timestamp())
