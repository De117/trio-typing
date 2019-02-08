from typing import (
    Any,
    AsyncContextManager,
    AsyncIterator,
    Awaitable,
    Callable,
    ContextManager,
    Coroutine,
    Generic,
    NoReturn,
    Optional,
    Sequence,
    Union,
    Sequence,
    TypeVar,
    Tuple,
)
from trio_typing import Nursery, ArgsForCallable, takes_callable_and_args
import trio
import outcome
import contextvars
import enum
import select

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

class _Statistics:
    def __getattr__(self, name: str) -> Any: ...

# _core._ki
def enable_ki_protection(fn: F) -> F: ...
def disable_ki_protection(fn: F) -> F: ...
def currently_ki_protected() -> bool: ...

# _core._entry_queue
class TrioToken:
    @takes_callable_and_args
    def run_sync_soon(
        self,
        sync_fn: Callable[[ArgsForCallable], None],
        *args: ArgsForCallable,
        idempotent: bool = False,
    ) -> None: ...

# _core._unbounded_queue
class UnboundedQueue(Generic[T]):
    def __init__(self) -> None: ...
    def qsize(self) -> int: ...
    def empty(self) -> bool: ...
    def put_nowait(self, obj: T) -> None: ...
    def get_batch_nowait(self) -> Sequence[T]: ...
    async def get_batch(self) -> Sequence[T]: ...
    def statistics(self) -> _Statistics: ...
    def __aiter__(self) -> AsyncIterator[Sequence[T]]: ...

# _core._run
class Task:
    coro: Coroutine[Any, outcome.Outcome[object], Any]
    name: str
    context: contextvars.Context
    custom_sleep_data: Any
    parent_nursery: Optional[Nursery]
    child_nurseries: Sequence[Nursery]

async def checkpoint() -> None: ...
async def checkpoint_if_cancelled() -> None: ...
def current_task() -> Task: ...
def current_root_task() -> Task: ...
def current_statistics() -> _Statistics: ...
def current_clock() -> trio.abc.Clock: ...
def current_trio_token() -> TrioToken: ...
def reschedule(task: Task, next_send: outcome.Outcome[Any] = ...) -> None: ...
@takes_callable_and_args
def spawn_system_task(
    async_fn: Callable[[ArgsForCallable], Awaitable[None]],
    *args: ArgsForCallable,
    name: object = ...,
) -> Task: ...
def add_instrument(instrument: trio.abc.Instrument) -> None: ...
def remove_instrument(instrument: trio.abc.Instrument) -> None: ...
async def wait_socket_readable(sock: trio.socket.SocketType) -> None: ...
async def wait_socket_writable(sock: trio.socket.SocketType) -> None: ...
def notify_socket_close(sock: trio.socket.SocketType) -> None: ...

# unix only
async def wait_readable(fd: int) -> None: ...
async def wait_writable(fd: int) -> None: ...
def notify_fd_close(fd: int) -> None: ...

# kqueue only
def current_kqueue() -> select.kqueue: ...
def monitor_kevent(
    ident: int, filter: int
) -> ContextManager[UnboundedQueue[select.kevent]]: ...
async def wait_kevent(
    ident: int, filter: int, abort_func: Callable[[Callable[[], NoReturn]], Abort]
) -> select.kevent: ...

# windows only
class _CompletionKeyEventInfo:
    lpOverlapped: int
    dwNumberOfBytesTransferred: int

def current_iocp() -> int: ...
def register_with_iocp(handle: int) -> None: ...
async def wait_overlapped(handle: int, lpOverlapped: int) -> None: ...
def monitor_completion_key() -> ContextManager[
    Tuple[int, UnboundedQueue[_CompletionKeyEventInfo]]
]: ...

# _core._traps
class Abort(enum.Enum):
    SUCCEEDED = ...
    FAILED = ...

async def cancel_shielded_checkpoint() -> None: ...
async def wait_task_rescheduled(
    abort_func: Callable[[Callable[[], NoReturn]], Abort]
) -> Any: ...
async def permanently_detach_coroutine_object(
    final_outcome: outcome.Outcome[object]
) -> Any: ...
async def temporarily_detach_coroutine_object(
    abort_func: Callable[[Callable[[], NoReturn]], Abort]
) -> Any: ...
async def reattach_detached_coroutine_object(task: Task, yield_value: Any) -> None: ...

# _core._parking_lot
class ParkingLot:
    def __len__(self) -> int: ...
    def __bool__(self) -> bool: ...
    async def park(self) -> None: ...
    def unpark(self, *, count: int = 1) -> Sequence[Task]: ...
    def unpark_all(self) -> Sequence[Task]: ...
    def repark(self, new_lot: ParkingLot, *, count: int = 1) -> None: ...
    def repark_all(self, new_lot: ParkingLot) -> None: ...
    def statistics(self) -> _Statistics: ...

# _core._local
class _RunVarToken:
    pass

class RunVar(Generic[T]):
    def __init__(self, name: str, default: T = ...) -> None: ...
    def get(self, default: T = ...) -> T: ...
    def set(self, value: T) -> _RunVarToken: ...
    def reset(self, token: _RunVarToken) -> None: ...

# _wait_for_object
async def WaitForSingleObject(obj: int) -> None: ...
