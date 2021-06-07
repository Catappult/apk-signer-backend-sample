from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Generic, Optional

T = TypeVar("T")
U = TypeVar("U")


class OperationStatus(Enum):
    SUCCESS = "SUCCESS"
    NOT_FOUND = "NOT_FOUND"
    ERROR = "ERROR"


@dataclass(frozen=True)
class OperationResult(Generic[T, U]):
    status: OperationStatus
    data: Optional[T] = None
    error_details: Optional[U] = None
