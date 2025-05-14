from sqlalchemy.types import TypeDecorator, Integer
from enum import Enum


class EnumIntegerType(TypeDecorator):
    impl = Integer
    cache_ok = True

    def __init__(self, enum_class: type[Enum], *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if isinstance(value, self.enum_class):
            return value.value
        elif isinstance(value, str):
            return self.enum_class[value].value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self.enum_class(value).name
        return value
