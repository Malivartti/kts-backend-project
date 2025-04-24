from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def values(cls) -> list[str]:
        return [str(item) for item in cls.__members__.values()]

    @classmethod
    def enum_values(cls) -> list:
        return list(cls.__members__.values())

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))
