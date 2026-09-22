from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("h4kfi")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__author__ = "digenaldo"
