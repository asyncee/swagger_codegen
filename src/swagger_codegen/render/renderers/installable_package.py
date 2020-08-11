from typing import List

from swagger_codegen.parsing.endpoint import EndpointDescription

from ..api import Api
from .package import PackageRenderer


class InstallablePackageRenderer(PackageRenderer):
    def __init__(
        self,
        *args,
        setup_py_template="package_renderer/setup_py.jinja2",
        manifest_in_template="package_renderer/manifest_in.jinja2",
        **kwargs,
    ):
        super(InstallablePackageRenderer, self).__init__(*args, **kwargs)

        self._package_dir = self._project_dir / self._package_name
        self._setup_py_template = setup_py_template
        self._manifest_in_template = manifest_in_template

    def render(self, endpoints: List[EndpointDescription]):
        super().render(endpoints)
        apis = self._get_apis(endpoints)
        self._render_setuptools(apis)

    def _render_setuptools(self, apis: List[Api]) -> None:
        """ Render files necessary for packaging the new client library with setuptools.
        """
        (self._project_dir / "README.md").write_text("# Client Library")
        ctx = {
            "package_name": self._package_name,
            "package_version": "1.0.0",
            "package_description": self._package_name,
        }
        # render <project>/setup.py
        (self._project_dir / "setup.py").write_text(
            self._render(self._setup_py_template, ctx)
        )
        # render <project>/MANIFEST.in necessary for setuptools auto-collector
        (self._project_dir / "MANIFEST.in").write_text(
            self._render(self._manifest_in_template, ctx)
        )
