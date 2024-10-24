from typing import Union
from pydantic import BaseModel, Field, model_validator
from redis.commands.core import ExpiryT, AbsExpiryT


class Config(BaseModel):
    ex: Union[ExpiryT, None] = Field(
        description="Expire the key after a specified number of seconds.",
        default=None
    )
    px: Union[ExpiryT, None] = Field(
        description="Expire the key after a specified number of milliseconds.",
        default=None
    )
    nx: bool = Field(
        description="Set the value only if the key does not exist.",
        default=False
    )
    xx: bool = Field(
        description="Set the value only if the key already exists.",
        default=False
    )
    keepttl: bool = Field(
        description="Retain the current time to live of the key.",
        default=False
    )
    get: bool = Field(
        description="Set the value and return the previous value, if any.",
        default=False
    )
    exat: Union[AbsExpiryT, None] = Field(
        description="Expire the key after a specified number of seconds from a specific timestamp.",
        default=None
    )
    pxat: Union[AbsExpiryT, None] = Field(
        description="Expire the key after a specified number of milliseconds from a specific timestamp.",
        default=None
    )

    @model_validator(mode='before')
    def convert_zeros_to_none(cls, values):
        for key, value in values.items():
            if value == "0":
                # print(value, type(value), "0 => None")
                values[key] = None
            else:
                ...
                # print(value, type(value))
        return values
