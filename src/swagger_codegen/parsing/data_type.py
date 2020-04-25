from __future__ import annotations

from typing import List
from typing import Optional

import attr


@attr.s
class DataType:
    python_type: Optional[str] = attr.ib()
    member_name: Optional[str] = attr.ib(default=None)
    member_value: Optional[str] = attr.ib(default=None)
    members: List[DataType] = attr.ib(factory=list)
    is_recursive: bool = attr.ib(default=False)
    is_optional_type: bool = attr.ib(default=False)

    @property
    def member_python_type(self) -> str:
        if not self.python_type.startswith("typing.Optional") and self.is_optional_type:
            return f"typing.Optional[{self.python_type}]"
        return self.python_type

    def is_object(self):
        return False

    def should_update_forward_refs(self):
        lookup = self.members.copy()

        for member in lookup:
            if self.python_type == member.python_type and member.is_recursive:
                return True
            lookup.extend(member.members)
        return False

    @classmethod
    def get_object_members(cls, data_type: DataType) -> List[DataType]:
        object_types = []

        if data_type.is_object() and not data_type.is_recursive:
            object_types.append(data_type)

        for member in data_type.members:
            object_types = cls.get_object_members(member) + object_types

        return object_types


@attr.s
class ObjectDataType(DataType):
    def is_object(self):
        return True
