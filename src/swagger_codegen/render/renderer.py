from typing import List

from swagger_codegen.parsing.endpoint import EndpointDescription
from swagger_codegen.render.post_processors.post_processor import PostProcessor
from swagger_codegen.render.templates import render_template


class Renderer:
    def render(self, endpoints: List[EndpointDescription]):
        raise NotImplementedError

    def add_post_processor(self, processor: PostProcessor):
        self._post_processors = getattr(self, "_post_processors", [])
        self._post_processors.append(processor)

    def _post_process(self, content: str) -> str:
        for processor in self._post_processors:
            content = processor.process(content)
        return content

    def _render(self, template_name: str, params: dict):
        content = render_template(template_name, params)
        return self._post_process(content)
