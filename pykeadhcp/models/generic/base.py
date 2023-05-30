from pydantic import BaseModel


def normalize_keys(string: str) -> str:
    return string.replace("_", "-")


class KeaBaseModel(BaseModel):
    class Config:
        alias_generator = normalize_keys
        allow_population_by_field_name = True
