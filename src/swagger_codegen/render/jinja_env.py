from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("swagger_codegen", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
