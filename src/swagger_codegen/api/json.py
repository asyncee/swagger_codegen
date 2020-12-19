import json

from pydantic.json import pydantic_encoder


class DefaultJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return pydantic_encoder(obj)
        except TypeError:
            pass
        return super().default(obj)


def dumps(*args, **kwargs):
    if "cls" not in kwargs:
        kwargs["cls"] = DefaultJSONEncoder
    return json.dumps(*args, **kwargs)
