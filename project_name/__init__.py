from .__version__ import __author__, __copyright__, __email__, __license__, __version__


def do_something(value: str) -> str:
    return value


def failed_func(value: str) -> None:
    raise ValueError("always failed")
