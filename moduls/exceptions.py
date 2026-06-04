from typing import final


@final
class RootWindowObjectAlreadyExistsException(Exception):
    ...
@final
class ServerInstanceAlreadyExists(Exception):
    ...

@final
class TheSocketWasNotTransferred(Exception):
    ...