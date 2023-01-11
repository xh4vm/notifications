from uuid import UUID


def str_if_uuid(value):
    return str(value) if isinstance(value, UUID) else value
