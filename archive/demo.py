from dataclasses import dataclass, field


class AugmentdTable:
    pass

@dataclass
class AugmentdTableSchema(AugmentdTable):
    pass

@dataclass
class Users(AugmentdTableSchema):
    id: str = field()
    name: str = field()
    email: str = field()


def generate_ddl(t: type[AugmentdTable])->str:
    for attr in getattrs(t):
        print (attr)

print(generate_ddl(Users))
