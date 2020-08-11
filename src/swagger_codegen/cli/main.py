import logging
from typing import Optional

import rich
import typer
from swagger_codegen.cli.config import load_config
from swagger_codegen.cli.imports import import_class, qualname
from swagger_codegen.cli.setup_renderer import setup_renderer
from swagger_codegen.parsing.endpoint import EndpointDescription
from swagger_codegen.parsing.loaders import load_base_schema
from swagger_codegen.parsing.parse import endpoints_from_base_schema
from swagger_codegen.render.renderers.package import PackageRenderer

from .setup_logging import setup_logging

app = typer.Typer()


logger = logging.getLogger(__name__)


@app.command()
def generate(
    uri: str,
    package: str,
    directory: Optional[str] = None,
    renderer: Optional[str] = None,
    endpoint: Optional[str] = None,
):
    directory = directory or "."
    renderer = renderer or qualname(PackageRenderer)
    endpoint = import_class(endpoint) if endpoint else EndpointDescription

    rich.print(
        f"Generating from [yellow]{uri}[/yellow] to [yellow]{directory} ({package})[/yellow]"
    )
    base_schema = load_base_schema(uri)
    rich.print(
        f"Loaded schema [yellow]{base_schema}[/yellow] "
        f"with {base_schema.endpoints_count} endpoint(s)"
    )

    endpoints = endpoints_from_base_schema(base_schema, endpoint)
    renderer = setup_renderer(renderer, directory=directory, package=package)
    renderer.render(list(endpoints))


@app.command()
def build(config: str = ".swagger_codegen.toml"):
    cfg = load_config(config)

    services = cfg.get("services", {})
    if not services:
        rich.print(f"[red]Nothing to build: no services defined in {config}[/red]")
        raise typer.Abort()

    endpoint_import_path = cfg.get("swagger_codegen", {}).get("endpoint")
    renderer_import_path = cfg.get("swagger_codegen", {}).get("renderer")

    for service_name, service_settings in services.items():
        try:
            generate(
                uri=service_settings["uri"],
                package=service_settings["package"],
                directory=service_settings.get("directory"),
                renderer=renderer_import_path,
                endpoint=endpoint_import_path,
            )
        except Exception:
            logger.exception("Failed to generate client for %r", service_name)


@app.callback()
def callback(loglevel: str = "INFO"):
    setup_logging(level=logging._nameToLevel[loglevel.upper()])


if __name__ == "__main__":
    app()
