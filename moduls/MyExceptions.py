from __future__ import annotations
from typing import final, TYPE_CHECKING

if TYPE_CHECKING:
    from .main_module import RootClass

class BaseRaiser():
    def __init__(self, RootClass: RootClass) -> None:
        RootClass

@final
class RootWindowObjectAlreadyExistsException(Exception):
    pass
@final
class ServerInstanceAlreadyExists():
    pass
@final
class TheSocketWasNotTransferred():
    pass
@final
class SocketMustBeSpecifed():
    pass
@final
class FakeRequestToStartGame():
    pass