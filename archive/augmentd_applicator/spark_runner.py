from archive.spark_delta_ops import run_query
from my_app.models.users import UsersEvents, RegisteredUsers, UsersLogs

users_events = UsersEvents()

registered_users = RegisteredUsers()

users_logs = UsersLogs()

TABLES = [users_events, registered_users, users_logs]

# init tables stage , create DDLs, topics etc...
for table in TABLES:
    if table.is_evolved:
        query = table.evolve_table()
        run_query(query)
