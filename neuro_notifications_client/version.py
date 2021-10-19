from importlib.metadata import version
from typing import Any


def __getattr__(name: str) -> Any:
    if name == "VERSION":
        global VERSION
        VERSION = version(__package__)
    else:
        raise AttributeError(f"Unknown attribute {name}")
