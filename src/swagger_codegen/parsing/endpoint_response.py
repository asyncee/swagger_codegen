import attr

from swagger_codegen.parsing.data_type import DataType


@attr.s(slots=True)
class EndpointResponse:
    status_code: str = attr.ib()
    data_type: DataType = attr.ib()
    definition: dict = attr.ib()
    content_type: str = attr.ib()
