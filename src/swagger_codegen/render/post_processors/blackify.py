import logging

from black import FileMode
from black import InvalidInput

from swagger_codegen.render.post_processors.post_processor import PostProcessor

logger = logging.getLogger(__name__)


class Blackify(PostProcessor):
    def process(self, content: str) -> str:
        try:
            return self._blackify_content(content)
        except InvalidInput as e:
            logger.error(e)

        return content

    def _blackify_content(self, content: str):
        try:
            import black
        except ImportError:
            return content

        return black.format_file_contents(content, fast=False, mode=FileMode(),)
