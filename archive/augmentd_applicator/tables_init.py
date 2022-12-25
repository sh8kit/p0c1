from augmentd.table_ops.events_ops import create_new_topic
from archive.spark_delta_ops import create_new_storage_table
from augmentd.tables import AugmentTableElement
from my_app.models.users import UsersEvents, RegisteredUsers, UsersLogs

users_events = UsersEvents()

registered_users = RegisteredUsers()

users_logs = UsersLogs()

TABLES = [users_events, registered_users, users_logs]

# init tables stage , create DDLs, topics etc...
for table in TABLES:
    if table.table_element == AugmentTableElement.STREAM:
        create_new_topic(table.table_name)
    if table.table_element == AugmentTableElement.STORAGE:
        if table.is_evolved:
            create_new_storage_table(table)
        else:
            create_new_storage_table(table)
