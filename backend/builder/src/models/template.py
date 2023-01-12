from pydantic import BaseModel


class TemplateDB(BaseModel):
    subject: str
    template_file: str


class Template(BaseModel):
    subject: str
    body: str
