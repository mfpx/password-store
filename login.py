import connector


class Login:

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def authenticate(self):
        dbptr = connector.DatabaseConnector().get_connection_object()
        queries = connector.DatabaseQueries(dbptr)

        result = queries.select_data({
            'operation': 'conditional_select',
            'table': 'users',
            'condition': '`username` = %s AND `master_password` = %s',
            'columns': ['username', 'created', 'uid'],
            'data': (self.username, self.password)
        })

        return result

