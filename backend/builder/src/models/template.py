from pydantic import BaseModel, Field


class TemplateDB(BaseModel):
    subject: str
    template_file: str


class Template(BaseModel):
    subject: str = Field(default="")
    body: str = Field(default="")
