from abc import ABC, abstractmethod
from typing import Any
from jinja2 import Environment, BaseLoader, Template


class BaseRenderer(ABC):
    @abstractmethod
    async def render(self, template: str, data: dict[str, Any], **kwargs) -> str:
        """Метод подстановки данных в шаблон"""


class Jinja2Renderer(BaseRenderer):
    async def render(self, template: str, data: dict[str, Any], **kwargs) -> str:
        _template: Template = Environment(enable_async=True, loader=BaseLoader).from_string(template)
        return await _template.render_async(**data)
