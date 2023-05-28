from typing import Optional, Union
from pydantic import BaseModel


class KeaResponse(BaseModel):
    result: int
    text: Optional[str]
    arguments: Optional[Union[dict, list]]
