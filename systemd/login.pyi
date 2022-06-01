from types import TracebackType
from typing import Final

from _typeshed import Self

__version__: Final[str]

def seats() -> list[str]: ...
def sessions() -> list[str]: ...
def machine_names() -> list[str]: ...
def uids() -> list[int]: ...

class Monitor:
    def __init__(self, category: str | None = ...) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    def fileno(self) -> int: ...
    def get_events(self) -> int: ...
    def get_timeout(self) -> int | None: ...
    def get_timeout_ms(self) -> int: ...
    def close(self) -> None: ...
    def flush(self) -> None: ...