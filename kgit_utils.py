def read_file(path):
    """Read contents of file at given path as bytes."""
    with open(path, mode="rb") as file:
        return file.read()


def write_file(path, data):
    """write bytes to given file."""
    with open(path, mode="wb") as file:
        file.write(data)
