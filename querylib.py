import connector

class Login:

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def authenticate(self) -> list:
        dbptr = connector.DatabaseConnector().get_connection_object()
        queries = connector.DatabaseQueries(dbptr)

        result = queries.select_data({
            'operation': 'conditional_select',
            'table': 'users',
            'condition': '`username` = %s AND `master_password` = PASSWORD(%s)',
            'columns': ['username', 'created', 'uid'],
            'data': (self.username, self.password)
        })

        return result


class Credentials:

    def __init__(self, username: str, uid: int = None) -> None:
        self.username = username
        self.uid = uid

    def __get_uid(self, username: str) -> str:
        if self.uid == None:
            dbptr = connector.DatabaseConnector().get_connection_object()
            queries = connector.DatabaseQueries(dbptr)

            result = queries.select_data({
                'operation': 'conditional_select',
                'table': 'users',
                'condition': '`username` = %s',
                'columns': ['uid'],
                'data': (self.username)
            })

            return result
        else:
            return self.uid

    def get(self) -> list:
        dbptr = connector.DatabaseConnector().get_connection_object()
        queries = connector.DatabaseQueries(dbptr)

        result = queries.select_data({
            'operation': 'conditional_select',
            'table': 'credentials',
            'condition': '`uid` = %s',
            'columns': ['*'],
            'data': (self.__get_uid(self.username)[0]['uid'])
        })

        return result