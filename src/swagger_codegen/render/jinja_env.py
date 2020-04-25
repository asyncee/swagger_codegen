from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape

env = Environment(
    loader=PackageLoader("swagger_codegen", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
