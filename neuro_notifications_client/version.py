from importlib.metadata import version
from typing import Any, Tuple


__all__ = ("VERSION",)


def __dir__() -> Tuple[str, ...]:
    return __all__


def __getattr__(name: str) -> Any:
    if name == "VERSION":
        global VERSION
        VERSION = version(__package__)  # type: ignore[name-defined]
    else:
        raise AttributeError(f"Unknown attribute {name}")
