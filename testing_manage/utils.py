def open_file(path, size=1024):
    with open(path, 'rb') as f:
        while True:
            data = f.read(size)
            if data:
                yield data
            else:
                break
