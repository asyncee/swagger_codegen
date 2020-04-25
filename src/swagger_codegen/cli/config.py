import toml


def load_config(name: str) -> dict:
    with open(name, "r") as f:
        return toml.load(f)
