from flask.json.provider import DefaultJSONProvider
from pydantic import BaseModel

def pydantic_to_dict(obj):
    """Рекурсивно превращает любые Pydantic-структуры в чистые dict/list."""
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, list):
        return [pydantic_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {k: pydantic_to_dict(v) for k, v in obj.items()}
    return obj

class PydanticJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        clean_obj = pydantic_to_dict(obj)
        return super().dumps(clean_obj, **kwargs)
