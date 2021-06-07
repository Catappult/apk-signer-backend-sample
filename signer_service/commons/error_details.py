from dataclasses import dataclass
from enum import Enum
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class ErrorType(Enum):
    NOT_FOUND = "NOT_FOUND"
    INVALID_INPUT = "INVALID_INPUT"


@dataclass(frozen=True)
class ErrorDetails(Generic[T]):
    type: ErrorType
    details: Optional[T] = None
