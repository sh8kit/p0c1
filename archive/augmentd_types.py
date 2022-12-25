from datetime import date, datetime
from enum import Enum


class AugmentTypes(Enum):
    STRING = str
    INTEGER = int
    TIMESTAMP = datetime
    DATE = date
