import logging

from swagger_codegen.render.post_processors.post_processor import PostProcessor

logger = logging.getLogger(__name__)


class Blackify(PostProcessor):
    def process(self, content: str) -> str:
        try:
            import black
        except ImportError:
            return content

        try:
            return black.format_file_contents(
                content, fast=False, mode=black.FileMode(),
            )
        except black.InvalidInput as e:
            logger.warning(
                f"Black failed to post-process file with an error: {e}. "
                f"Currently it happens on non python files, "
                f"you can safely ignore this message."
            )

        return content
