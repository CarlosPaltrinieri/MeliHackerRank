from typing import Any, Optional
from pydantic import BaseModel

class ResponseExtension(BaseModel):
    status_code: int
    message: Optional[str] = None
    data: Optional[Any] = None

    @classmethod
    def response(cls, status_code: int, data: Any = None, message: str = None):
        return cls(status_code=status_code, data=data, message=message)
