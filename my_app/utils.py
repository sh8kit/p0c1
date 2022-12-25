from datetime import datetime, date
from typing import Dict, Any

from datashack.entities.tables import Table
import random
import string


def random_string() -> str:
    # choose from all lowercase letter
    length = int(random.random() * 10)
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def random_date() -> date:
    return random_datetime().date()


def random_datetime() -> datetime:
    return datetime.now()


def random_number() -> float:
    return random.random() * 1000000


def fake_data_generator(table: Table) -> Dict[str, Any]:
    columns = table.columns
    data = {}
    for c_name in columns:
        c_type = columns[c_name].col_type
        if c_type == str:
            data[c_name] = random_string()
        elif c_type == datetime:
            data[c_name] = random_datetime()
        elif c_type == date:
            data[c_name] = random_date()
        elif c_type in (int, float):
            data[c_name] = c_type(random_number())
    return data
