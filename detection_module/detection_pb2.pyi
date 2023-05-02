from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ["ip_address"]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ip_address: str
    def __init__(self, ip_address: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: bool
    def __init__(self, status: bool = ...) -> None: ...
