import re
from enum import Enum


class AugmentTableElement(Enum):
    STREAM = "stream"
    STORAGE = "storage"


STORAGE_MAP = {
    AugmentTableElement.STORAGE: "DELTA"
}


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()