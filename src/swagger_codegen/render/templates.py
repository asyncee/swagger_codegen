from .jinja_env import env


def render_template(name: str, params) -> str:
    return env.get_template(name).render(**params)
