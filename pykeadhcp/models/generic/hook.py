from typing import Optional
from pydantic import BaseModel


class Hook(BaseModel):
    library: str
    parameters: Optional[dict]
    name: Optional[str]
