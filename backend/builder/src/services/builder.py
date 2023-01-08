from abc import ABC, abstractmethod
from typing import Any
from jinja2 import Environment, BaseLoader, Template


class BaseBuilder(ABC):

    @abstractmethod
    async def build(self, template: str, data: dict[str, Any], **kwargs) -> str:
        '''Метод подстановки данных в шаблон'''


class JinjaBuilder(BaseBuilder):

    async def build(self, template: str, data: dict[str, Any], **kwargs) -> str:
        _template: Template = Environment(loader=BaseLoader).from_string(template)
        return await _template.render_async(**data)
