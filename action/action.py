from abc import abstractmethod
import json

from pydantic import BaseModel

class BaseAction(BaseModel):

    @property
    @abstractmethod
    def run_on_server(self) -> bool:
      pass

    def __init_subclass__(cls, **kwargs):
      super().__init_subclass__(**kwargs)
      if not hasattr(cls, 'run_on_server'):
        raise TypeError(f'{cls.__name__} must define "run_on_server" property.')


    def to_json(self) -> str:
      return self.model_dump_json(indent=2)

    @classmethod
    def serialize_fields(cls):
      fields = {}
      for base in cls.__mro__:
        if hasattr(base, '__annotations__'):
          fields.update(base.__annotations__)
      return fields

    @classmethod
    def from_json(cls, json_string: str):
      return cls.model_validate_json(json_string)

