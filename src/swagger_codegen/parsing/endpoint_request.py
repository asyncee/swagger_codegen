import attr

from swagger_codegen.parsing.data_type import DataType


@attr.s(slots=True)
class EndpointRequest:
    name: str = attr.ib()
    data_type: DataType = attr.ib()
    definition: dict = attr.ib()
    content_type: str = attr.ib()
