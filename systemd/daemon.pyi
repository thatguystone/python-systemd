from socket import AddressFamily, SocketKind
from typing import Final, Literal, Sequence, TypeAlias

from _typeshed import FileDescriptorLike

SocketType: TypeAlias = SocketKind | Literal[0]

_RawListening: TypeAlias = Literal[-1] | Literal[0] | Literal[1]
_PyListening: TypeAlias = bool | None
Listening: TypeAlias = _PyListening | _RawListening

__version__: Final[str]
LISTEN_FDS_START: Final[int]

def booted() -> bool: ...
def notify(
    status: str,
    unset_environment: bool = ...,
    pid: int = ...,
    fds: Sequence[int] | None = ...,
) -> bool: ...
def is_fifo(fileobj: FileDescriptorLike, path: str | None = ...) -> bool: ...
def is_socket(
    fileobj: FileDescriptorLike,
    family: AddressFamily = ...,
    type: SocketType = ...,
    listening: Listening = ...,
) -> bool: ...
def is_socket_inet(
    fileobj: FileDescriptorLike,
    family: AddressFamily = ...,
    type: SocketType = ...,
    listening: Listening = ...,
    port: int = ...,
) -> bool: ...
def is_socket_sockaddr(
    fileobj: FileDescriptorLike,
    address,
    type: SocketType = ...,
    flowinfo: int = ...,
    listening: Listening = ...,
) -> bool: ...
def is_socket_unix(
    fileobj: FileDescriptorLike,
    type: SocketType = ...,
    listening: Listening = ...,
    path: str | None = ...,
) -> bool: ...
def is_mq(fileobj: FileDescriptorLike, path: str | None = ...) -> bool: ...
def listen_fds(unset_environment: bool = ...) -> list[int]: ...
def listen_fds_with_names(unset_environment: bool = ...) -> dict[int, str]: ...
