from datetime import datetime, timedelta
from enum import IntEnum, IntFlag
from logging import Handler, _Level, LogRecord
from types import TracebackType
from typing import (
    Any,
    Callable,
    Final,
    Iterator,
    NamedTuple,
    Protocol,
    Sequence,
    TypeAlias,
    TypedDict,
)
from uuid import UUID

from _typeshed import Self

__version__: Final[str]

class StateChange(IntEnum):
    NOP: int
    APPEND: int
    INVALIDATE: int

NOP: StateChange
APPEND: StateChange
INVALIDATE: StateChange

class Flag(IntFlag):
    LOCAL_ONLY: int
    RUNTIME_ONLY: int
    SYSTEM: int
    SYSTEM_ONLY: int
    CURRENT_USER: int
    OS_ROOT: int

LOCAL_ONLY: Flag
RUNTIME_ONLY: Flag
SYSTEM: Flag
SYSTEM_ONLY: Flag
CURRENT_USER: Flag
OS_ROOT: Flag

class LogLevel(IntEnum):
    LOG_EMERG = int
    LOG_ALERT = int
    LOG_CRIT = int
    LOG_ERR = int
    LOG_WARNING = int
    LOG_NOTICE = int
    LOG_INFO = int
    LOG_DEBUG = int

LOG_EMERG: LogLevel
LOG_ALERT: LogLevel
LOG_CRIT: LogLevel
LOG_ERR: LogLevel
LOG_WARNING: LogLevel
LOG_NOTICE: LogLevel
LOG_INFO: LogLevel
LOG_DEBUG: LogLevel

class Monotonic(NamedTuple):
    timestamp: timedelta
    bootid: UUID

Converter: TypeAlias = Callable[[bytes], Any]
Converters: TypeAlias = dict[str, Converter]

DEFAULT_CONVERTERS: Converters

class _Entry(TypedDict, total=False):
    _AUDIT_LOGINUID: int
    _AUDIT_SESSION: int
    _BOOT_ID: UUID
    _GID: int
    _MACHINE_ID: UUID
    _PID: int
    _SOURCE_MONOTONIC_TIMESTAMP: timedelta
    _SOURCE_REALTIME_TIMESTAMP: datetime
    _SYSTEMD_OWNER_UID: int
    _SYSTEMD_SESSION: int
    _UID: int
    CODE_LINE: int
    COREDUMP_GID: int
    COREDUMP_PID: int
    COREDUMP_SESSION: int
    COREDUMP_SIGNAL: int
    COREDUMP_TIMESTAMP: datetime
    COREDUMP_UID: int
    COREDUMP: bytes
    ERRNO: int
    EXIT_STATUS: int
    INITRD_USEC: int
    KERNEL_USEC: int
    LEADER: int
    MESSAGE_ID: UUID
    MESSAGE: str
    PRIORITY: LogLevel
    SESSION_ID: int
    SYSLOG_FACILITY: int
    SYSLOG_PID: int
    USERSPACE_USEC: int

class Entry(_Entry):
    __CURSOR: str
    __MONOTONIC_TIMESTAMP: Monotonic
    __REALTIME_TIMESTAMP: datetime

class EmptyEntry(TypedDict):
    pass

class Reader:
    converters: Converters

    def __init__(
        self,
        flags: Flag = ...,
        path: int | str | bytes = ...,
        files: Sequence[int] | Sequence[str | bytes] = ...,
        namespace: str | bytes = ...,
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    def __iter__(self) -> Iterator[Entry]: ...
    def __next__(self) -> Entry: ...
    def fileno(self) -> int: ...
    def reliable_fd(self) -> int: ...
    def get_events(self) -> int: ...
    def get_timeout(self) -> int | None: ...
    def get_timeout_ms(self) -> int: ...
    def close(self) -> None: ...
    def get_usage(self) -> int: ...
    def add_match(self, *args: str, **kwargs: str) -> None: ...
    def add_disjunction(self) -> None: ...
    def add_conjunction(self) -> None: ...
    def flush_matches(self) -> None: ...
    def seek_head(self) -> None: ...
    def seek_tail(self) -> None: ...
    def seek_realtime(self, realtime: datetime | float) -> None: ...
    def seek_monotonic(
        self, monotonic: timedelta | float, bootid: bytes | None = ...
    ) -> None: ...
    def process(self) -> StateChange: ...
    def wait(self, timeout: float = ...) -> StateChange: ...
    def seek_cursor(self, cursor: str) -> None: ...
    def test_cursor(self, cursor: str) -> bool: ...
    def query_unique(self, field: str) -> set[bytes]: ...
    def enumerate_fields(self) -> set[str]: ...
    def has_runtime_files(self) -> bool: ...
    def has_persistent_files(self) -> bool: ...
    def get_catalog(self) -> str: ...
    @property
    def data_threshold(self) -> int: ...
    @data_threshold.setter
    def data_threshold(self, val: int) -> None: ...
    @property
    def closed(self) -> bool: ...
    def get_next(self, skip: int = ...) -> Entry | EmptyEntry: ...
    def get_previous(self, skip: int = ...) -> Entry | EmptyEntry: ...
    def log_level(self, level: LogLevel) -> None: ...
    def messageid_match(self, messageid: str | UUID) -> None: ...
    def this_boot(self, bootid: str | UUID | None = ...) -> None: ...
    def this_machine(self, machineid: str | UUID | None = ...) -> None: ...

def get_catalog(mid: str | UUID) -> str: ...
def stream(
    identifier: str | None = ...,
    priority: LogLevel = ...,
    level_prefix: bool = ...,
) -> int: ...

class SenderFunction(Protocol):
    def __call__(
        self,
        MESSAGE: str,
        MESSAGE_ID: str | UUID | None = ...,
        CODE_FILE: str | None = ...,
        CODE_LINE: int | None = ...,
        CODE_FUNC: str | None = ...,
        **kwargs: str | bytes | Any,
    ) -> None: ...

send: SenderFunction = ...

class JournalHandler(Handler):
    send: SenderFunction

    def __init__(
        self,
        level: _Level = ...,
        sender_function: SenderFunction = ...,
        **kwargs: object,
    ) -> None: ...
    @classmethod
    def with_args(cls, config: dict[str, str] | None = ...): ...
    def emit(self, record: LogRecord) -> None: ...
    @staticmethod
    def map_priority(levelno: _Level) -> LogLevel: ...
    @staticmethod
    def mapPriority(levelno: _Level) -> LogLevel: ...
