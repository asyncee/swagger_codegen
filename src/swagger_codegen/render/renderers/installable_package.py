import os
from pathlib import Path
from pkg_resources import get_distribution
from typing import List

from inflection import underscore
from swagger_codegen.parsing.endpoint import EndpointDescription

from .package import PackageRenderer


class InstallablePackageRenderer(PackageRenderer):
    def __init__(
        self,
        *args,
        setup_py_template="package_renderer/setup_py.jinja2",
        manifest_in_template="package_renderer/manifest_in.jinja2",
        readme_template="package_renderer/readme.jinja2",
        **kwargs,
    ):
        super(InstallablePackageRenderer, self).__init__(*args, **kwargs)

        self._project_dir = self._directory / self._package_name
        self._valid_python_package_name = underscore(self._package_name)
        # second level of nesting is necessary to separate `setup.py` and meta-files (readme, tests etc)
        # from the package files (runtime modules)
        self._package_dir = self._project_dir / self._valid_python_package_name
        self._package_api_lib_name = "lib"
        self._package_api_lib_module_name = f"{self._valid_python_package_name}.{self._package_api_lib_name}"

        self._setup_py_template = setup_py_template
        self._manifest_in_template = manifest_in_template
        self._readme_template = readme_template

    def render(self, endpoints: List[EndpointDescription]):
        super().render(endpoints)
        self._render_setuptools()

    def _render_setuptools(self) -> None:
        """ Render files necessary for packaging the new client library with setuptools.
        """
        (self._project_dir / "README.md").write_text(
            self._render(
                self._readme_template,
                {
                    "package_name": self._valid_python_package_name,
                    "pypi_name": self._package_name,
                    "package_api_lib_module_name": self._package_api_lib_module_name,
                }
            )
        )
        ctx = {
            "package_name": self._valid_python_package_name,
            "pypi_name": self._package_name,
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

    def _render_low_level_lib(self, codegen_distribution: str) -> None:
        """ Render ``swagger_codegen.api`` as ``<package_name>.lib``.
        This way we make the generated client package independent from ``swagger_codegen``,
        which saves our runtime from unnecessary dependencies in production.
        """
        dist = get_distribution(codegen_distribution)
        src_lib_name = f'{codegen_distribution}.api'.encode('utf-8')
        lib_location = Path(dist.location) / codegen_distribution / 'api'
        lib = lib_location.rglob('*.py')
        for src in lib:
            lib_src = src.read_bytes().replace(src_lib_name, self._package_api_lib_module_name.encode('utf-8'))
            lib_path = self._package_api_lib_dir / src.relative_to(lib_location)
            if os.sep in str(lib_path):
                lib_path.parent.mkdir(parents=True, exist_ok=True)
            lib_path.write_bytes(lib_src)
