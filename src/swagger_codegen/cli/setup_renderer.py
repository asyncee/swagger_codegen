from swagger_codegen.cli.imports import import_class
from swagger_codegen.render.post_processors.blackify import Blackify


def setup_renderer(import_path: str, **kwargs):
    renderer_class = import_class(import_path)
    renderer = renderer_class(**kwargs)
    renderer.add_post_processor(Blackify())
    return renderer
