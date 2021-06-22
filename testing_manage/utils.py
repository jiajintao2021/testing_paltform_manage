import datetime


def open_file(path, size=1024):
    with open(path, 'rb') as f:
        while True:
            data = f.read(size)
            if data:
                yield data
            else:
                break


def now_date():
    return datetime.datetime.now().date().strftime('%Y-%m-%d')


def now_date_30():
    return (datetime.datetime.now().date() + datetime.timedelta(days=-30)).strftime('%Y-%m-%d')
