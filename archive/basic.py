from dataclasses import dataclass

from augmentd.tables import camel_to_snake


class SHACK:
    @classmethod
    def merge(cls, other, on, how="INNER"):
        return (cls, f"{how} JOIN {other.table_name} on {camel_to_snake(cls.table_name)}.{on}=={camel_to_snake(other.table_name)}.{on}")
