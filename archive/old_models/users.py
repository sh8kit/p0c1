from archive.basic import SHACK
from augmentd.tables import augmentd_table, AugmentedCol
from archive.augmentd_types import AugmentTypes


@augmentd_table  # TODO set later table_type=AugmentTableElement.STREAM and create kafka interface
class UsersEvents(SHACK):
    id: AugmentTypes.STRING = AugmentedCol(default=AugmentTypes.STRING)
    action: AugmentTypes.STRING = AugmentedCol(default=AugmentTypes.STRING)
    event_ts: AugmentTypes.TIMESTAMP = AugmentedCol(default=AugmentTypes.TIMESTAMP)


@augmentd_table
class RegisteredUsers(SHACK):
    id: AugmentTypes.STRING = AugmentedCol(default=AugmentTypes.STRING)
    full_name: AugmentTypes.STRING = AugmentedCol(default=AugmentTypes.STRING)
    email: AugmentTypes.STRING = AugmentedCol(default=AugmentTypes.STRING)


@augmentd_table(is_evolved=True)
class UsersLogs(SHACK):
    _evolve = UsersEvents.merge(other=RegisteredUsers, on="id")

    id: RegisteredUsers.id = AugmentedCol(source=RegisteredUsers)  # TODO didnt know how to get anotation type from the original table so i set it as param
    full_name: RegisteredUsers.full_name = AugmentedCol(source=RegisteredUsers)
    email: RegisteredUsers.email = AugmentedCol(source=RegisteredUsers)
    action: UsersEvents.action = AugmentedCol(source=UsersEvents)
    event_ts: UsersEvents.event_ts = AugmentedCol(source=UsersEvents)
