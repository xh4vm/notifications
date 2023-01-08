import re

from django.conf import settings


def validate_doctype(value: str):
    return value.strip() in settings.EVENT_TEMPLATE_DOCTYPE


def validate_template(value: str):
    result = re.search(settings.EVENT_TEMPLATE_PATTERN, value, re.S)
    return bool(result)


def get_template_params(value: str) -> list:
    result = re.findall(settings.EVENT_TEMPLATE_PARAMS_PATTERN, value)
    return result
