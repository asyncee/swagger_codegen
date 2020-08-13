import shutil
from collections import defaultdict
from pathlib import Path
from typing import List
from typing import Set

from swagger_codegen.parsing.data_type import DataType
from swagger_codegen.parsing.endpoint import EndpointDescription
from ..api import Api
from ..renderer import Renderer
from ..templates import render_template
from ..utils import to_classname
from ..utils import to_identifier


class PackageRenderer(Renderer):
    def __init__(
        self,
        directory: str,
        package: str,
        api_template="package_renderer/api.jinja2",
        endpoint_template="package_renderer/endpoint.jinja2",
        endpoint_dto_template="package_renderer/dto.jinja2",
        client_template="package_renderer/client.jinja2",
        endpoint_imports_template="package_renderer/endpoint_imports.jinja2",
        package_entrypoint_template="package_renderer/package_entrypoint.jinja2",
    ):
        self._directory = Path(directory).resolve()

        if not self._directory.exists():
            raise ValueError(f"Directory {directory!r} does not exist")

        if not self._directory.is_dir():
            raise ValueError(f"{directory!r} is not a directory")

        if not package or package == ".":
            raise ValueError(f"{package!r} is invalid package name")

        self._package_name = package
        self._project_dir = self._directory / self._package_name
        self._package_dir = self._project_dir

        # name of a subpackage inside a generated client that provides a lower-level HTTP API implementation
        self._package_api_lib_name = "api"
        self._package_api_lib_module_name = f"swagger_codegen.{self._package_api_lib_name}"

        self._api_template = api_template
        self._endpoint_template = endpoint_template
        self._endpoint_dto_template = endpoint_dto_template
        self._client_template = client_template
        self._endpoint_imports_template = endpoint_imports_template
        self._package_entrypoint_template = package_entrypoint_template

    @property
    def _package_api_lib_dir(self) -> Path:
        return self._package_dir / self._package_api_lib_name

    def render(self, endpoints: List[EndpointDescription]):
        if self._package_dir.exists():
            shutil.rmtree(self._package_dir)
        self._package_dir.mkdir(parents=True, exist_ok=False)

        apis = self._get_apis(endpoints)

        for api in apis:
            self._render_api(api)

        self._render_client(apis)
        self._render_low_level_lib('swagger_codegen')

    def _get_apis(self, endpoints: List[EndpointDescription]) -> List[Api]:
        endpoints_by_tags = defaultdict(list)

        for endpoint in endpoints:
            for tag in endpoint.tags:
                endpoints_by_tags[tag].append(endpoint)

        apis = []

        for tag, endpoints in endpoints_by_tags.items():
            name = to_identifier(tag)
            typename = to_classname(tag) + "Api"
            apis.append(Api(name=name, type_name=typename, endpoints=endpoints))

        return apis

    def _render_client(self, apis: List[Api]):
        (self._package_dir / "__init__.py").write_text(
            self._render(
                self._package_entrypoint_template,
                {"package_api_lib_module_name": self._package_api_lib_module_name}
            )
        )

        content = self._render(
            self._client_template,
            {
                "apis": apis,
                "package_api_lib_module_name": self._package_api_lib_module_name,
            }
        )
        (self._package_dir / "client.py").write_text(content)

    def _render_api(self, api: Api):
        api_dir = self._package_dir / "apis" / api.name
        api_dir.mkdir(parents=True, exist_ok=True)
        (api_dir / "__init__.py").touch()

        api_py_content = self._render(
            self._api_template,
            {
                "api": api,
                "package_api_lib_module_name": self._package_api_lib_module_name,
            }
        )
        (api_dir / "api.py").write_text(api_py_content)

        for endpoint in api.endpoints:
            self._render_endpoint(api_dir, endpoint)

    def _render_endpoint(self, api_dir: str, endpoint: EndpointDescription):
        imports_block = render_template(
            self._endpoint_imports_template,
            {"package_api_lib_module_name": self._package_api_lib_module_name}
        )
        data_types_block = []
        data_types_to_render: List[DataType] = []

        if endpoint.body_request:
            data_types_to_render.extend(
                DataType.get_object_members(endpoint.body_request.data_type)
            )
        for response in endpoint.responses:
            data_types_to_render.extend(DataType.get_object_members(response.data_type))

        _rendered_types: Set[str] = set()
        for data_type in data_types_to_render:
            if data_type.python_type not in _rendered_types:
                data_types_block.append(
                    render_template(self._endpoint_dto_template, {"type": data_type})
                )
                _rendered_types.add(data_type.python_type)

        endpoint_block = render_template(
            self._endpoint_template, {"endpoint": endpoint}
        )

        endpoint_content = "\n".join([imports_block, *data_types_block, endpoint_block])
        endpoint_content = self._post_process(endpoint_content)

        (api_dir / endpoint.name).with_suffix(".py").write_text(endpoint_content)

    def _render_low_level_lib(self, codegen_distribution: str) -> None:
        """ do nothing to preserve backward compatibility
        """
        return
