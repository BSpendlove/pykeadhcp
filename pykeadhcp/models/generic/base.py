from typing import Optional
from pydantic import BaseModel


def normalize_keys(string: str) -> str:
    return string.replace("_", "-")


class KeaBaseModel(BaseModel):
    class Config:
        alias_generator = normalize_keys
        allow_population_by_field_name = True
        use_enum_values = True


class KeaModel(KeaBaseModel):
    user_context: Optional[dict]
    comment: Optional[str]
    unknown_map_entry: Optional[str]
